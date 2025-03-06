import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolutiofiBurnTokensTool(BaseTool):
    name: str = "solutiofi_burn_tokens"
    description: str = """
    Burns tokens for a given list of mints using SolutiofiManager.

    Input: A JSON string with:
    {
        "mints": "list, a list of mint addresses"
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
                "mints": {"type": list, "required": True}
            }
            validate_input(data, schema)
            
            transaction_details = await self.agent_kit.burn_tokens(
                mints=data["mints"]
            )
            return {
                "transaction_details": transaction_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_details": None,
                "message": f"Error burning tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")