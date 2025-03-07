import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class LightProtocolSendCompressedAirdropTool(BaseTool):
    name: str = "lightprotocol_send_compressed_airdrop"
    description: str = """
    Sends a compressed airdrop using LightProtocolManager.

    Input: A JSON string with:
    {
        "mint_address": "string, the mint address of the token",
        "amount": "float, the amount to send",
        "decimals": "int, the number of decimal places for the token",
        "recipients": "list, the list of recipient addresses",
        "priority_fee_in_lamports": "int, the priority fee in lamports",
        "should_log": "bool, optional, whether to log the transaction"
    }
    Output:
    {
        "transaction_ids": "list, transaction IDs of the airdrop",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "mint_address": {"type": str, "required": True},
                "amount": {"type": float, "required": True},
                "decimals": {"type": int, "required": True},
                "recipients": {"type": list, "required": True},
                "priority_fee_in_lamports": {"type": int, "required": True},
                "should_log": {"type": bool, "required": False}
            }
            validate_input(data, schema)
            
            transaction_ids = await self.solana_kit.send_compressed_airdrop(
                mint_address=data["mint_address"],
                amount=data["amount"],
                decimals=data["decimals"],
                recipients=data["recipients"],
                priority_fee_in_lamports=data["priority_fee_in_lamports"],
                should_log=data.get("should_log", False)
            )
            return {
                "transaction_ids": transaction_ids,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_ids": None,
                "message": f"Error sending compressed airdrop: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

