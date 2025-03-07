import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class VirtualsGetSentientListingsTool(BaseTool):
    name: str = "virtuals_get_sentient_listings"
    description: str = """
    Fetches Sentient listings using VirtualsManager.

    Input: A JSON string with:
    {
        "page_number": "int, optional, the page number for pagination (default: 1)",
        "page_size": "int, optional, the number of items per page (default: 30)"
    }
    Output:
    {
        "listings": "dict, the listings data",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "page_number": int,
                "page_size": int
            }
            validate_input(data, schema)

            listings = await self.agent_kit.get_sentient_listings(
                page_number=data.get("page_number", 1),
                page_size=data.get("page_size", 30)
            )
            return {
                "listings": listings,
                "message": "Success"
            }
        except Exception as e:
            return {
                "listings": None,
                "message": f"Error fetching Sentient listings: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsBuySentientTool(BaseTool):
    name: str = "virtuals_buy_sentient"
    description: str = """
    Purchases Sentient tokens using VirtualsManager.

    Input: A JSON string with:
    {
        "token_address": "string, the token address",
        "amount": "string, the amount to purchase",
        "builder_id": "int, optional, the builder ID for the purchase"
    }
    Output:
    {
        "transaction_receipt": "dict, the transaction receipt",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "token_address": str,
                "amount": str,
                "builder_id": int
            }
            validate_input(data, schema)
            
            transaction_receipt = await self.agent_kit.buy_sentient(
                token_address=data["token_address"],
                amount=data["amount"],
                builder_id=data.get("builder_id")
            )
            return {
                "transaction_receipt": transaction_receipt,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_receipt": None,
                "message": f"Error purchasing Sentient tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsSellSentientTool(BaseTool):
    name: str = "virtuals_sell_sentient"
    description: str = """
    Sells Sentient tokens using VirtualsManager.

    Input: A JSON string with:
    {
        "token_address": "string, the token address",
        "amount": "string, the amount to sell",
        "builder_id": "int, optional, the builder ID for the sale"
    }
    Output:
    {
        "transaction_receipt": "dict, the transaction receipt",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "token_address": str,
                "amount": str,
                "builder_id": int
            }
            validate_input(data, schema)
            
            transaction_receipt = await self.agent_kit.sell_sentient(
                token_address=data["token_address"],
                amount=data["amount"],
                builder_id=data.get("builder_id")
            )
            return {
                "transaction_receipt": transaction_receipt,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_receipt": None,
                "message": f"Error selling Sentient tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
