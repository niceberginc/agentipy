from agentipy.agent import SolanaAgentKit
from agentipy.langchain.oracle.get_price import StorkGetPriceTool


def get_stork_tools(solana_kit: SolanaAgentKit):
    return [
        StorkGetPriceTool(solana_kit=solana_kit)
    ]