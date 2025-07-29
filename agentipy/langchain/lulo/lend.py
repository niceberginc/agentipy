import json

from langchain.tools import BaseTool
from solders.pubkey import Pubkey  # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class LuloLendTool(BaseTool):
    name: str = "lulo_lend"
    description: str = """
    Lends tokens for yields using Lulo with LuloManager.

    Input: A JSON string with:
    {
        "mint_address": "string, the SPL mint address of the token",
        "amount": "float, the amount to lend"
    }
    Output:
    {
        "transaction_signature": "string, the transaction signature",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "mint_address": {"type": str, "required": True},
                "amount": {"type": float, "required": True}
            }
            validate_input(data, schema)
            transaction_signature = await self.agent_kit.lulo_lend(
                mint_address=data["mint_address"],
                amount=data["amount"]
            )
            return {
                "transaction_signature": transaction_signature,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_signature": None,
                "message": f"Error lending asset using Lulo: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class LuloLendAssetsTool(BaseTool):
    name: str = "lulo_lend_assets"
    description: str = """
    Lends assets for yields using Lulo with LuloManager.

    Input: A JSON string with:
    {
        "amount": "float, the amount to lend",
    }
    Output:
    {
        "transaction_signature": "string, the transaction signature",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "amount": {"type": float, "required": True}
            }
            validate_input(data, schema)
            transaction_signature = await self.agent_kit.lend_assets(
                amount=data["amount"]
            )
            return {
                "transaction_signature": transaction_signature,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_signature": None,
                "message": f"Error lending assets using Lulo: {str(e)}"
            }
        