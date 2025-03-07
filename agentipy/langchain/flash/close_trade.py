import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class FlashCloseTradeTool(BaseTool):
    name: str = "flash_close_trade"
    description: str = """
    Closes a flash trade using the Solana Agent toolkit API.

    Input: A JSON string with:
    {
        "token": "string, the trading token",
        "side": "string, either 'buy' or 'sell'"
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
                "side": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)         
            transaction = await self.solana_kit.flash_close_trade(
                token=data["token"],
                side=data["side"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error closing flash trade: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

