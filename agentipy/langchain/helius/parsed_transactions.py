import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class SolanaHeliusGetParsedTransactionsTool(BaseTool):
    name: str = "solana_helius_get_parsed_transactions"
    description: str = """
    Fetch parsed transactions for a list of transaction IDs.

    Input: A JSON string with:
    {
        "signatures": ["string, the transaction signatures"],
        "commitment": "optional commitment level"
    }

    Output:
    {
        "parsed_transactions": "list of parsed transactions"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "signatures": {"type": list, "required": True},
                "commitment": {"type": str, "required": False}
            }
            validate_input(data, schema)

            signatures = data["signatures"]
            commitment = data.get("commitment")

            result = await self.solana_kit.get_parsed_transactions(signatures, commitment)
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
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
