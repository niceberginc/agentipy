from agentipy.agent import SolanaAgentKit
from agentipy.langchain.raydium.buy import SolanaRaydiumBuyTool
from agentipy.langchain.raydium.sell import SolanaRaydiumSellTool


def get_raydium_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaRaydiumBuyTool(solana_kit=solana_kit),
        SolanaRaydiumSellTool(solana_kit=solana_kit)
    ]
