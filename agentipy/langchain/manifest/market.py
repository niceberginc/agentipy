import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class ManifestWithdrawAllTool(BaseTool):
    name: str = "manifest_withdraw_all"
    description: str = """
    Withdraws all assets from a given market using ManifestManager.

    Input: A JSON string with:
    {
        "market_id": "string, the market ID"
    }
    Output:
    {
        "withdrawal_result": "dict, details of the withdrawal",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "market_id": {"type": str, "required": True}
            }
            validate_input(data, schema)
            withdrawal_result = await self.solana_kit.withdraw_all(
                market_id=data["market_id"]
            )
            return {
                "withdrawal_result": withdrawal_result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "withdrawal_result": None,
                "message": f"Error withdrawing all assets: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class OpenBookCreateMarketTool(BaseTool):
    name: str = "openbook_create_market"
    description: str = """
    Creates a new OpenBook market using OpenBookManager.

    Input: A JSON string with:
    {
        "base_mint": "string, the base mint address",
        "quote_mint": "string, the quote mint address",
        "lot_size": "float, optional, the lot size (default: 1)",
        "tick_size": "float, optional, the tick size (default: 0.01)"
    }
    Output:
    {
        "market_data": "dict, the created market details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "base_mint": {"type": str, "required": True},
                "quote_mint": {"type": str, "required": True},
                "lot_size": {"type": float, "required": False},
                "tick_size": {"type": float, "required": False}
            }
            market_data = await self.solana_kit.create_openbook_market(
                base_mint=data["base_mint"],
                quote_mint=data["quote_mint"],
                lot_size=data.get("lot_size", 1),
                tick_size=data.get("tick_size", 0.01)
            )
            return {
                "market_data": market_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "market_data": None,
                "message": f"Error creating OpenBook market: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
