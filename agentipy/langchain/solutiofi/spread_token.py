import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolutiofiSpreadTokenTool(BaseTool):
    name: str = "solutiofi_spread_token"
    description: str = """
    Spreads a token for a given list of target mints using SolutiofiManager.

    Input: A JSON string with:
    {
        "input_asset": "dict, the input asset details",
        "target_tokens": "list, a list of target token dictionaries",
        "priority_fee": "string, the priority fee"
    }
    Output:
    {
        "transaction_details": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "input_asset": {"type": dict, "required": True},
                "target_tokens": {"type": list, "required": True},
                "priority_fee": {"type": str, "required": True}
            }
            validate_input(data, schema)
            transaction_details = await self.agent_kit.spread_token(
                input_asset=data["input_asset"],
                target_tokens=data["target_tokens"],
                priority_fee=data["priority_fee"]
            )
            return {
                "transaction_details": transaction_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_details": None,
                "message": f"Error spreading token: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")