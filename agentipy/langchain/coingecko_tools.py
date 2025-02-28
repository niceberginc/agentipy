import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool

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

    async def _arun(self, input: str):
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

class CoingeckoGetTokenPriceDataTool(BaseTool):
    name: str = "coingecko_get_token_price_data"
    description: str = """
    Fetches token price data from CoinGecko using CoingeckoManager.

    Input: A JSON string with:
    {
        "token_addresses": "list, the list of token contract addresses"
    }
    Output:
    {
        "price_data": "dict, the token price data",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "token_addresses": {"type": list, "required": True}
            }
            validate_input(data, schema)
            price_data = await self.agent_kit.get_token_price_data(
                token_addresses=data["token_addresses"]
            )
            return {
                "price_data": price_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "price_data": None,
                "message": f"Error fetching token price data: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class CoingeckoGetTokenInfoTool(BaseTool):
    name: str = "coingecko_get_token_info"
    description: str = """
    Fetches token info from CoinGecko using CoingeckoManager.

    Input: A JSON string with:
    {
        "token_address": "string, the token's contract address"
    }
    Output:
    {
        "token_info": "dict, the token info data",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "token_address": {"type": str, "required": True}
            }
            validate_input(data, schema)
            token_info = await self.agent_kit.get_token_info(
                token_address=data["token_address"]
            )
            return {
                "token_info": token_info,
                "message": "Success"
            }
        except Exception as e:
            return {
                "token_info": None,
                "message": f"Error fetching token info: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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

    async def _arun(self, input: str):
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


def get_coingecko_tools(agent_kit: SolanaAgentKit):
    return [
        CoingeckoGetTrendingTokensTool(agent_kit=agent_kit),
        CoingeckoGetTrendingPoolsTool(agent_kit=agent_kit),
        CoingeckoGetTopGainersTool(agent_kit=agent_kit),
    ]

