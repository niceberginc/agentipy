import json

from langchain.tools import BaseTool
from solders.pubkey import Pubkey  # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaSellPumpfunTokenTool(BaseTool):
    name: str = "solana_sell_token"
    description: str = """
    Sell a specific amount of tokens using the bonding curve.

    Input: A JSON string with:
    {
        "mint": "The mint address of the token as a string",
        "bonding_curve": "The bonding curve public key as a string",
        "associated_bonding_curve": "The associated bonding curve public key as a string",
        "amount": "The amount of tokens to sell",
        "slippage": "The allowed slippage percentage",
        "max_retries": "Maximum retries for the transaction"
    }

    Output:
    {
        "status": "success",
        "transaction": "Details of the successful transaction"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:    
            data = json.loads(input)
            schema = {
                "mint": {"type": str, "required": True},
                "bonding_curve": {"type": str, "required": True},
                "associated_bonding_curve": {"type": str, "required": True},
                "amount": {"type": int, "required": True, "min": 1},
                "slippage": {"type": float, "required": False, "min": 0, "max": 100},
                "max_retries": {"type": int, "required": False, "min": 1}
            }
            validate_input(data, schema)

            mint = Pubkey(data["mint"])
            bonding_curve = Pubkey(data["bonding_curve"])
            associated_bonding_curve = Pubkey(data["associated_bonding_curve"])
            amount = data["amount"]
            slippage = data.get("slippage", 0.5)
            max_retries = data.get("max_retries", 3)

            result = await self.solana_kit.sell_token(
                mint, bonding_curve, associated_bonding_curve, amount, slippage, max_retries
            )
            return {
                "status": "success",
                "transaction": result.dict(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution.")
