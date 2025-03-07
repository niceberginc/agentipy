from agentipy.agent import SolanaAgentKit
from agentipy.langchain.faucet.solana_request_funds import SolanaFaucetTool


def get_faucet_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaFaucetTool(solana_kit=solana_kit),
    ]  