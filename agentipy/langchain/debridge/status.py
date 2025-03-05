import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaDeBridgeCheckTransactionStatusTool(BaseTool):
    name: str = "debridge_check_transaction_status"
    description: str = """
    Checks the status of a DeBridge transaction.

    Input: A JSON string with:
    {
        "tx_hash": "string, the transaction hash"
    }

    Output:
    {
        "status": "string, the transaction status",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "tx_hash": {"type": str, "required": True}
            }
            validate_input(data, schema)

            tx_hash = data["tx_hash"]

            status = await self.solana_kit.check_transaction_status(tx_hash)
            return {
                "status": status,
                "message": "Success"
            }
        except Exception as e:
            return {
                "status": None,
                "message": f"Error checking transaction status: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
