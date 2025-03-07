import json

from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool

from agentipy.helpers import validate_input


class CoingeckoGetTopGainersTool(BaseTool):
    name: str = "coingecko_get_top_gainers"
    description: str = """
    Fetches top gainers from CoinGecko using CoingeckoManager.

    Input: A JSON string with:
    {
        "duration": "string, optional, the duration filter for top gainers (default: '24h')",
        "top_coins": "int or string, optional, the number of top coins to return (default: 'all')"
    }
    Output:
    {
        "top_gainers": "dict, the top gainers data",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "duration": {"type": str, "required": False},
                "top_coins": {"type": (int, str), "required": False}
            }
            validate_input(data, schema)
            top_gainers = await self.agent_kit.get_top_gainers(
                duration=data.get("duration", "24h"),
                top_coins=data.get("top_coins", "all")
            )
            return {
                "top_gainers": top_gainers,
                "message": "Success"
            }
        except Exception as e:
            return {
                "top_gainers": None,
                "message": f"Error fetching top gainers: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
