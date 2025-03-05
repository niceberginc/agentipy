import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class FlashOpenTradeTool(BaseTool):
    name: str = "flash_open_trade"
    description: str = """
    Opens a flash trade using the Solana Agent toolkit API.

    Input: A JSON string with:
    {
        "token": "string, the trading token",
        "side": "string, either 'buy' or 'sell'",
        "collateralUsd": "float, collateral amount in USD",
        "leverage": "float, leverage multiplier"
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
                "token": {"type": str, "required": True},
                "side": {"type": str, "required": True},
                "collateralUsd": {"type": float, "required": True},
                "leverage": {"type": float, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
           
            transaction = await self.solana_kit.flash_open_trade(
                token=data["token"],
                side=data["side"],
                collateral_usd=data["collateralUsd"],
                leverage=data["leverage"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error opening flash trade: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")
