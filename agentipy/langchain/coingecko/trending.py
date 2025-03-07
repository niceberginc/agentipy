from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class CoingeckoGetTrendingTokensTool(BaseTool):
    name: str = "coingecko_get_trending_tokens"
    description: str = """
    Fetches trending tokens from CoinGecko using CoingeckoManager.

    Input: None
    Output:
    {
        "trending_tokens": "dict, the trending tokens data",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self):
        try:
            trending_tokens = await self.agent_kit.get_trending_tokens()
            
            return {
                "trending_tokens": trending_tokens,
                "message": "Success"
            }
        except Exception as e:
            return {
                "trending_tokens": None,
                "message": f"Error fetching trending tokens: {str(e)}"
            }

    def _run(self, ):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
