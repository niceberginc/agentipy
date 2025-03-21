import asyncio
import json
import logging
from typing import Any, Dict

import mcp.server.stdio
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.types import TextContent, Tool

from agentipy.agent import SolanaAgentKit
from agentipy.mcp.all_actions import ALL_ACTIONS
from agentipy.mcp.type import ActionType

logger = logging.getLogger("agentipy-mcp-server")

class AgentipyMCPServer:
    def __init__(self, agent: SolanaAgentKit, selected_actions: Dict[str, Any] = None, server_name="agentipy-mcp"):
        self.server = Server(server_name)
        self.agent = agent

        self.selected_actions = selected_actions or ALL_ACTIONS

        self.server.list_tools()(self.list_tools)
        self.server.call_tool()(self.call_tool)

    async def list_tools(self) -> list[Tool]:
        """Returns only selected tools."""
        return [
            Tool(
                name=action.name,
                description=action.description,
                inputSchema=action.schema,
            )
            for action in self.selected_actions.values()
        ]

    async def call_tool(self, name: str, arguments: dict):
        """Executes the selected tool dynamically."""
        if name not in self.selected_actions:
            return [TextContent(type="text", text=f"Unknown action: {name}")]

        action = self.selected_actions[name]
        try:
            result = await action.handler(self.agent, arguments)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            logger.error(f"Error executing {name}: {str(e)}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    async def run(self):
        """Starts the MCP server."""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=self.server.name,
                    server_version="1.0",
                    capabilities=self.server.get_capabilities(notification_options=NotificationOptions()),
                ),
            )

def start_mcp_server(agent: SolanaAgentKit, selected_actions: Dict[str, Any] = None):
    """Allows users to start MCP with only their selected actions."""
    server = AgentipyMCPServer(agent, selected_actions)
    asyncio.run(server.run())
