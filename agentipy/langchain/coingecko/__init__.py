from agentipy.agent import SolanaAgentKit
from agentipy.langchain.coingecko.gainers import CoingeckoGetTopGainersTool
from agentipy.langchain.coingecko.pools import (CoingeckoGetLatestPoolsTool,
                                                CoingeckoGetTrendingPoolsTool)
from agentipy.langchain.coingecko.token_data import (
    CoingeckoGetTokenInfoTool, CoingeckoGetTokenPriceDataTool)
from agentipy.langchain.coingecko.trending import \
    CoingeckoGetTrendingTokensTool


def get_coingecko_tools(solana_kit: SolanaAgentKit):
    return [
        CoingeckoGetTopGainersTool(agent_kit=solana_kit),
        CoingeckoGetLatestPoolsTool(agent_kit=solana_kit),
        CoingeckoGetTrendingPoolsTool(agent_kit=solana_kit),
        CoingeckoGetTokenInfoTool(agent_kit=solana_kit),
        CoingeckoGetTokenPriceDataTool(agent_kit=solana_kit),
        CoingeckoGetTrendingTokensTool(agent_kit=solana_kit)
    ]