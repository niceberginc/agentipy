import os
from agentipy import SolanaAgentKit
from agentipy.mcp.mcp_server import start_mcp_server, ALL_ACTIONS

def main():
    agent = SolanaAgentKit(
        private_key=os.getenv("SOLANA_PRIVATE_KEY"),
        rpc_url=os.getenv("RPC_URL"),
    )

    # Use all available actions or specify a subset
    selected_actions = ALL_ACTIONS

    start_mcp_server(agent, selected_actions)

if __name__ == "__main__":
    main()
