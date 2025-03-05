import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaHeliusGetBalancesTool(BaseTool):
    name: str = "solana_helius_get_balances"
    description: str = """
    Fetch the balances for a given Solana address.

    Input: A JSON string with:
    {
        "address": "string, the Solana address"
    }

    Output: {
        "balances": List[dict], # the list of token balances for the address
        "status": "success" or "error",
        "message": "Error message if any"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "address": {"type": str, "required": True}
            }
            validate_input(data, schema)

            address = data["address"]

            result = await self.solana_kit.get_balances(address)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
