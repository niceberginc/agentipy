import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class SolanaHeliusGetRawTransactionsTool(BaseTool):
    name: str = "solana_helius_get_raw_transactions"
    description: str = """
    Fetch raw transactions for a list of accounts.

    Input: A JSON string with:
    {
        "signatures": ["string, the transaction signatures"],
        "start_slot": "optional start slot",
        "end_slot": "optional end slot",
        "start_time": "optional start time",
        "end_time": "optional end time",
        "limit": "optional limit",
        "sort_order": "optional sort order",
        "pagination_token": "optional pagination token"
    }

    Output:
    {
        "transactions": "list of raw transactions"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "signatures": {"type": list, "required": True},
                "start_slot": {"type": int, "required": False},
                "end_slot": {"type": int, "required": False},
                "start_time": {"type": int, "required": False},
                "end_time": {"type": int, "required": False},
                "limit": {"type": int, "required": False},
                "sort_order": {"type": str, "required": False},
                "pagination_token": {"type": str, "required": False}
            }
            validate_input(data, schema)

            signatures = data["signatures"]
            start_slot = data.get("start_slot")
            end_slot = data.get("end_slot")
            start_time = data.get("start_time")
            end_time = data.get("end_time")
            limit = data.get("limit")
            sort_order = data.get("sort_order")
            pagination_token = data.get("pagination_token")

            result = await self.solana_kit.get_raw_transactions(
                signatures, start_slot, end_slot, start_time, end_time, limit, sort_order, pagination_token
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

