import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class VirtualsBuyPrototypeTool(BaseTool):
    name: str = "virtuals_buy_prototype"
    description: str = """
    Purchases Prototype tokens using VirtualsManager.

    Input: A JSON string with:
    {
        "token_address": "string, the token address",
        "amount": "string, the amount to purchase",
        "builder_id": "int, optional, the builder ID for the purchase",
        "slippage": "float, optional, the slippage tolerance percentage"
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
            transaction_receipt = await self.agent_kit.buy_prototype(
                token_address=data["token_address"],
                amount=data["amount"],
                builder_id=data.get("builder_id"),
                slippage=data.get("slippage")
            )
            return {
                "transaction_receipt": transaction_receipt,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_receipt": None,
                "message": f"Error purchasing Prototype tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsSellPrototypeTool(BaseTool):
    name: str = "virtuals_sell_prototype"
    description: str = """
    Sells Prototype tokens using VirtualsManager.

    Input: A JSON string with:
    {
        "token_address": "string, the token address",
        "amount": "string, the amount to sell",
        "builder_id": "int, optional, the builder ID for the sale",
        "slippage": "float, optional, the slippage tolerance percentage"
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
            
            transaction_receipt = await self.agent_kit.sell_prototype(
                token_address=data["token_address"],
                amount=data["amount"],
                builder_id=data.get("builder_id"),
                slippage=data.get("slippage")
            )
            return {
                "transaction_receipt": transaction_receipt,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_receipt": None,
                "message": f"Error selling Prototype tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
