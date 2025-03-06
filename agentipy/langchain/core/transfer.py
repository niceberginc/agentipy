import json

from langchain.tools import BaseTool
from solders.pubkey import Pubkey  # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaTransferTool(BaseTool):
    name:str = "solana_transfer"
    description:str = """
    Transfer tokens or SOL to another address.

    Input (JSON string):
    {
        "to": "wallet_address",
        "amount": 1,
        "mint": "mint_address" (optional)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {  
                "to": {"type": str, "required": True},
                "amount": {"type": int, "required": True, "min": 1},
                "mint": {"type": str, "required": False}
            }
            validate_input(data, schema)

            recipient = Pubkey.from_string(data["to"])
            mint_address = data.get("mint") and Pubkey.from_string(data["mint"])

            transaction = await self.solana_kit.transfer(recipient, data["amount"], mint_address)

            return {
                "status": "success",
                "message": "Transfer completed successfully",
                "amount": data["amount"],
                "recipient": data["to"],
                "token": data.get("mint", "SOL"),
                "transaction": transaction,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
    def _run(self):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

