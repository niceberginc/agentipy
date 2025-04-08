import logging

from agentipy.agent import SolanaAgentKit
from agentipy.agent.evm import EvmAgentKit
from agentipy.langchain import create_solana_tools
from agentipy.langchain.evm import create_evm_tools
from agentipy.mcp.all_actions import ALL_ACTIONS
from agentipy.mcp.mcp_server import start_mcp_server

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

__all__ = ["SolanaAgentKit", "create_solana_tools","start_mcp_server", "ALL_ACTIONS", "EvmAgentKit", "create_evm_tools"]
