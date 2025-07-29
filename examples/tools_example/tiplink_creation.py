import logging
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_tiplink import TiplinkManager

logging.basicConfig(level=logging.INFO)

def test_create_tiplink():
    agent = SolanaAgentKit(
        private_key="",
        rpc_url="https://api.devnet.solana.com",
        openai_api_key="",
        solutiofi_api_key=""
    )

    print("Creating Tiplink...")
    result = TiplinkManager.create_tiplink(agent, amount=0.01)
    print("Tiplink Result:", result)

if __name__ == "__main__":
    test_create_tiplink()
