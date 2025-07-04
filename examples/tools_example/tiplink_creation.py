import logging
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_tiplink import TiplinkManager

logging.basicConfig(level=logging.INFO)

def test_create_tiplink():
    agent = SolanaAgentKit(
        private_key="23nna8ixFP4s4aJAMw5bUAh84Nkw7EyByc3YYiSokcDFtqgAz35xt34TMiFAGPzRoEe6suC9qYedpzfAo3VGBRWb",
        rpc_url="https://api.devnet.solana.com",
        openai_api_key="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",
        solutiofi_api_key="479d31e1-1ec2-4d73-b9b6-90324bba39cd"
    )

    print("Creating Tiplink...")
    result = TiplinkManager.create_tiplink(agent, amount=0.01)
    print("Tiplink Result:", result)

if __name__ == "__main__":
    test_create_tiplink()
