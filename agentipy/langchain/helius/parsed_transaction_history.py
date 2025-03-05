import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class SolanaHeliusGetParsedTransactionHistoryTool(BaseTool):
    name: str = "solana_helius_get_parsed_transaction_history"
    description: str = """
    Fetch parsed transaction history for a given address.

    Input: A JSON string with:
    {
        "address": "string, the account address",
        "before": "optional before transaction timestamp",
        "until": "optional until transaction timestamp",
        "commitment": "optional commitment level",
        "source": "optional source of transaction",
        "type": "optional type of transaction"
    }

    Output:
    {
        "transaction_history": "list of parsed transaction history"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "address": {"type": str, "required": True},
                "before": {"type": str, "required": False},
                "until": {"type": str, "required": False},
                "commitment": {"type": str, "required": False},
                "source": {"type": str, "required": False},
                "type": {"type": str, "required": False}
            }
            validate_input(data, schema)

            address = data["address"]
            before = data.get("before", "")
            until = data.get("until", "")
            commitment = data.get("commitment", "")
            source = data.get("source", "")
            type = data.get("type", "")

            result = await self.solana_kit.get_parsed_transaction_history(
                address, before, until, commitment, source, type
            )
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
