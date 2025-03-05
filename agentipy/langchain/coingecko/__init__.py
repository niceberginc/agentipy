from agentipy.agent import SolanaAgentKit
from agentipy.langchain.coingecko.pools import CoingeckoGetPoolsTool
from agentipy.langchain.coingecko.token_data import CoingeckoGetTokenDataTool
from agentipy.langchain.coingecko.gainers import CoingeckoGetGainersTool
from agentipy.langchain.coingecko.trending import CoingeckoGetTrendingTool


def get_coingecko_tools(solana_kit: SolanaAgentKit):
    return [
        CoingeckoGetPoolsTool(solana_kit=solana_kit),
        CoingeckoGetTokenDataTool(solana_kit=solana_kit),
        CoingeckoGetGainersTool(solana_kit=solana_kit),
        CoingeckoGetTrendingTool(solana_kit=solana_kit)
    ]