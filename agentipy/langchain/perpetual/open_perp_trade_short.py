import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class OpenPerpTradeShortTool(BaseTool):
    name: str = "open_perp_trade_short"
    description: str = """
    Opens a perpetual short trade.

    Input: A JSON string with:
    {
        "price": "float, entry price for the trade",
        "collateral_amount": "float, amount of collateral",
        "collateral_mint": "string, optional, mint address of the collateral",
        "leverage": "float, optional, leverage factor",
        "trade_mint": "string, optional, token mint address",
        "slippage": "float, optional, slippage tolerance"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "price": {"type": float, "required": True},
                "collateral_amount": {"type": float, "required": True},
                "collateral_mint": {"type": str, "required": False},
                "leverage": {"type": float, "required": False},
                "trade_mint": {"type": str, "required": False},
                "slippage": {"type": float, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)

            transaction = await self.solana_kit.open_perp_trade_short(  
                price=data["price"],
                collateral_amount=data["collateral_amount"],
                collateral_mint=data.get("collateral_mint"),
                leverage=data.get("leverage"),
                trade_mint=data.get("trade_mint"),
                slippage=data.get("slippage")
            )
           
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error opening perp short trade: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
 
