import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class VoltrGetPositionValuesTool(BaseTool):
    name: str = "voltr_get_position_values"
    description: str = """
    Retrieves position values for a given vault in Voltr.

    Input: A JSON string with:
    {
        "vault": "string, the vault address"
    }

    Output:
    {
        "position_values": "dict, position values",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "vault": {"type": str, "required": True},
            }
            validate_input(data, schema)

            vault = data["vault"]

            result = await self.solana_kit.get_position_values(vault)
            return {
                "status": "success",
                "position_values": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")