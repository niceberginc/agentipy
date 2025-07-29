# mcp_sse_server.py
import json
import logging
import shlex
from contextlib import asynccontextmanager
from typing import Dict, Union

import uvicorn
from mcp.server import Server
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.sse import SseServerTransport
from mcp.types import TextContent, Tool
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route

logger = logging.getLogger("mcp-sse")

mcp = FastMCP("agentipy-sse-mcp-server")

def parse_key_value_string(s: str) -> dict:
    try:
        return dict(part.split("=", 1) for part in shlex.split(s))
    except Exception as e:
        raise ValueError(f"Invalid key=value string: {e}")

def normalize_kwargs(raw: Union[str, dict]) -> dict:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        raw = raw.strip()
        if raw.startswith("{"):
            try:
                raw = json.loads(raw)
                if isinstance(raw, str):
                    raw = json.loads(raw)
                return raw
            except Exception as e:
                raise ValueError(f"Invalid JSON format in 'kwargs': {e}")
        else:
            return parse_key_value_string(raw)
    raise ValueError(f"Unsupported kwargs type: {type(raw)}")

def register_tools(tool_dict: Dict[str, Tool]):
    for name, tool in tool_dict.items():
        def bind_tool(tool_name, tool_def):
            @mcp.tool(name=tool_name, description=tool_def.description)
            async def _tool(ctx: Context, **kwargs):
                try:
                    # Extract agent from request state
                    request = getattr(mcp, "request", None)
                    if not request or not hasattr(request.state, "agent"):
                        raise ValueError("Missing request or agent")

                    agent = request.state.agent

                    # Normalize kwargs
                    if "kwargs" in kwargs:
                        kwargs = normalize_kwargs(kwargs["kwargs"])

                    # Detect whether this is a ctx-based tool or an agent/params-based tool
                    handler_params = tool_def.handler.__code__.co_varnames

                    if "ctx" in handler_params:
                        # ctx-based (e.g. custom dynamic workflows)
                        result = await tool_def.handler(ctx, **kwargs)
                    else:
                        # legacy style (agent + params)
                        result = await tool_def.handler(agent, kwargs)

                    return TextContent(type="text", text=json.dumps(result, indent=2))

                except Exception as e:
                    logger.error(f"Error in tool {tool_name}: {str(e)}")
                    await ctx.error(f"Error running tool: {str(e)}")
                    return TextContent(type="text", text=f"Error: {str(e)}")

        bind_tool(name, tool)


@asynccontextmanager
async def patch_request(mcp_server: Server, request: Request):
    mcp_server.request = request
    try:
        yield
    finally:
        del mcp_server.request

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
            mcp.request = request

            try:
                options = mcp_server.create_initialization_options()
                await mcp_server.run(
                    read_stream,
                    write_stream,
                    options,
                )
            finally:
                del mcp.request

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

def start_sse_server(tools: Dict[str, Tool], host="127.0.0.1", port=3001):
    register_tools(tools)
    app = create_starlette_app(mcp._mcp_server, debug=True)
    logger.info(f"Server running on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

def build_sse_starlette_app(tools: Dict[str, Tool], debug=True) -> Starlette:
    register_tools(tools)
    return create_starlette_app(mcp._mcp_server, debug=debug)
