import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaSendTxn(BaseTool):
    name: str = "send_txn"
    description: str = """
    Send an individual transaction to the Jito network for processing.

    Input: A JSON string with:
    {
        "txn_signature": "string, the transaction signature",
        "bundleOnly": "boolean, whether to send the transaction as a bundle"
    }

    Output:
    {
        "status": "Unique identifier of the processed transaction bundle"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "txn_signature": {"type": str, "required": True},
                "bundleOnly": {"type": bool, "required": True}
            }
            validate_input(data, schema)

            txn_signature = data["txn_signature"]
            bundleOnly = data["bundleOnly"]
            result = await self.solana_kit.send_txn(txn_signature, bundleOnly)
            return {
                "status": result
            }
        except Exception as e:
            return {
                "status": None
            }

    def _run(self):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
