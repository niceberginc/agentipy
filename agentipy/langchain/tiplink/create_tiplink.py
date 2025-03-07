import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class TiplinkCreateTool(BaseTool):
    name: str = "tiplink_create"
    description: str = """
    Creates a TipLink on Solana.

    Input: A JSON string with:
    {
        "amount": "float, the tip amount",
        "spl_mint_address": "string, optional, the SPL mint address"
    }

    Output:
    {
        "transaction_details": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "amount": {"type": float, "required": True},
                "spl_mint_address": {"type": str, "required": False},
            }
            validate_input(data, schema)

            amount = data["amount"]
            spl_mint_address = data.get("spl_mint_address")

            result = await self.solana_kit.create_tiplink(amount, spl_mint_address)
            return {
                "status": "success",
                "transaction_details": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
