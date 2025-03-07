import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolayerRestakeTool(BaseTool):
    name: str = "solayer_restake"
    description: str = """
    Restakes all rewards using SolayerManager.

    Input: A JSON string with:
    {
        "amount": "float, the amount to restake"
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
            schema = {
                "amount": {"type": float, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            transaction_signature = await self.agent_kit.restake(
                amount=data["amount"]
            )
            return {
                "transaction_signature": transaction_signature,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_signature": None,
                "message": f"Error restaking rewards using Solayer: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
