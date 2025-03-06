import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


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

