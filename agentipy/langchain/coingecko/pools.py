import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class CoingeckoGetLatestPoolsTool(BaseTool):
    name: str = "coingecko_get_latest_pools"
    description: str = """
    Fetches the latest pools from CoinGecko for the Solana network using CoingeckoManager.

    Input: None
    Output:
    {
        "latest_pools": "dict, the latest pools data",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self):
        try:
            latest_pools = await self.agent_kit.get_latest_pools()
            return {
                "latest_pools": latest_pools,
                "message": "Success"
            }
        except Exception as e:
            return {
                "latest_pools": None,
                "message": f"Error fetching latest pools: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class CoingeckoGetTrendingPoolsTool(BaseTool):
    name: str = "coingecko_get_trending_pools"
    description: str = """
    Fetches trending pools from CoinGecko for the Solana network using CoingeckoManager.

    Input: A JSON string with:
    {
        "duration": "string, optional, the duration filter for trending pools (default: '24h'). Allowed values: '5m', '1h', '6h', '24h'."
    }
    Output:
    {
        "trending_pools": "dict, the trending pools data",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "duration": {"type": str, "required": False}
            }
            validate_input(data, schema)
            trending_pools = await self.agent_kit.get_trending_pools(
                duration=data.get("duration", "24h")
            )
            return {
                "trending_pools": trending_pools,
                "message": "Success"
            }
        except Exception as e:
            return {
                "trending_pools": None,
                "message": f"Error fetching trending pools: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

  