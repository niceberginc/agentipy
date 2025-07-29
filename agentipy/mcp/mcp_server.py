import inspect
import json
import logging
import shlex
from typing import Dict, List, Union

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import TextContent, Tool

from agentipy.agent import SolanaAgentKit
from agentipy.mcp.all_actions import ALL_ACTIONS

logger = logging.getLogger("agentipy-mcp-server")

mcp = FastMCP(
    "agentipy-mcp",
    instructions="Solana tools: Get balance, transfer SOL, price prediction, etc.",
    dependencies=["pydantic", "httpx", "solana"],
)

def parse_key_value_string(s: str) -> dict:
    try:
        return dict(part.split("=", 1) for part in shlex.split(s))
    except Exception as e:
        raise ValueError(f"Invalid key=value string: {e}")

async def list_tools(selected_actions: Dict[str, Tool]) -> List[Tool]:
    return [
        Tool(
            name=action.name,
            description=action.description,
            inputSchema=action.inputSchema,
        )
        for action in selected_actions.values()
    ]

async def call_tool(agent: SolanaAgentKit, selected_actions: Dict[str, Tool], name: str, arguments: dict):
    if name not in selected_actions:
        return [TextContent(type="text", text=f"Unknown action: {name}")]

    action = selected_actions[name]
    try:
        result = action.handler(agent, arguments)

        if inspect.isawaitable(result):
            result = await result

        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        logger.error(f"Error executing {name}: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

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

def run_server(agent: SolanaAgentKit, selected_actions: Dict[str, Tool], server_name="agentipy-mcp"):
    logger.info(f'Starting MCP server with {list(selected_actions.keys())} actions')

    for name, tool in selected_actions.items():
        def register_tool(tool_name, tool_def):
            @mcp.tool(name=tool_name, description=tool_def.description)
            async def _tool(ctx: Context, **kwargs):
                try:
                    if "kwargs" in kwargs:
                        kwargs = normalize_kwargs(kwargs["kwargs"])

                    result = tool_def.handler(agent, kwargs)
                    
                    if inspect.isawaitable(result):
                        result = await result

                    return TextContent(type="text", text=json.dumps(result, indent=2))
                except Exception as e:
                    logger.error(f"Error in tool '{tool_name}': {str(e)}")
                    logger.error(f"Error in tool {tool_name} with kwargs {kwargs}")
                    await ctx.error(f"Error running tool: {str(e)}")
                    return TextContent(type="text", text=f"Error: {str(e)}")
        register_tool(name, tool)

    mcp.run()

def start_mcp_server(agent: SolanaAgentKit, selected_actions: Dict[str, Tool] = None):
    selected = selected_actions or ALL_ACTIONS
    run_server(agent, selected)
