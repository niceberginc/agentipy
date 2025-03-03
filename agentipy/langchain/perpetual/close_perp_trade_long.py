import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class ClosePerpTradeLongTool(BaseTool):
    name: str = "close_perp_trade_long"
    description: str = """
    Closes a perpetual long trade.

    Input: A JSON string with:
    {
        "price": "float, execution price for closing the trade",
        "trade_mint": "string, token mint address for the trade"
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
                "trade_mint": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)

            price = data["price"]
            trade_mint = data["trade_mint"]
            
            transaction = await self.solana_kit.close_perp_trade_long(
                price=price,
                trade_mint=trade_mint
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error closing perp long trade: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
