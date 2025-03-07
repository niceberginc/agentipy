import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolutiofiMergeTokensTool(BaseTool):
    name: str = "solutiofi_merge_tokens"
    description: str = """
    Merges tokens for a given list of mints using SolutiofiManager.

    Input: A JSON string with:
    {
        "input_assets": "list, a list of input asset dictionaries",
        "output_mint": "string, the output mint address",
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
                "input_assets": {"type": list, "required": True},
                "output_mint": {"type": str, "required": True},
                "priority_fee": {"type": str, "required": True}
            }
            validate_input(data, schema)
            transaction_details = await self.agent_kit.merge_tokens(
                input_assets=data["input_assets"],
                output_mint=data["output_mint"],
                priority_fee=data["priority_fee"]
            )
            return {
                "transaction_details": transaction_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_details": None,
                "message": f"Error merging tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
