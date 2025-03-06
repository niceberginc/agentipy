import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class ManifestCreateMarketTool(BaseTool):
    name: str = "manifest_create_market"
    description: str = """
    Creates a new market using ManifestManager.

    Input: A JSON string with:
    {
        "base_mint": "string, the base mint address",
        "quote_mint": "string, the quote mint address"
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
                "quote_mint": {"type": str, "required": True}
            }
            validate_input(data, schema)
            market_data = await self.solana_kit.create_manifest_market(
                base_mint=data["base_mint"],
                quote_mint=data["quote_mint"]
            )
            return {
                "market_data": market_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "market_data": None,
                "message": f"Error creating market: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class ManifestPlaceLimitOrderTool(BaseTool):
    name: str = "manifest_place_limit_order"
    description: str = """
    Places a limit order on a market using ManifestManager.

    Input: A JSON string with:
    {
        "market_id": "string, the market ID",
        "quantity": "float, the quantity to trade",
        "side": "string, 'buy' or 'sell'",
        "price": "float, the price per unit"
    }
    Output:
    {
        "order_details": "dict, the placed order details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "market_id": {"type": str, "required": True},
                "quantity": {"type": float, "required": True},
                "side": {"type": str, "required": True},
                "price": {"type": float, "required": True}
            }
            validate_input(data, schema)
            order_details = await self.solana_kit.place_limit_order(
                market_id=data["market_id"],
                quantity=data["quantity"],
                side=data["side"],
                price=data["price"]
            )
            return {
                "order_details": order_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "order_details": None,
                "message": f"Error placing limit order: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class ManifestPlaceBatchOrdersTool(BaseTool):
    name: str = "manifest_place_batch_orders"
    description: str = """
    Places multiple batch orders on a market using ManifestManager.

    Input: A JSON string with:
    {
        "market_id": "string, the market ID",
        "orders": "list, a list of orders (each order must include 'quantity', 'side', and 'price')"
    }
    Output:
    {
        "batch_order_details": "dict, details of the placed batch orders",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "market_id": {"type": str, "required": True},
                "orders": {"type": list, "required": True}
            }
            validate_input(data, schema)
            batch_order_details = await self.solana_kit.place_batch_orders(
                market_id=data["market_id"],
                orders=data["orders"]
            )
            return {
                "batch_order_details": batch_order_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "batch_order_details": None,
                "message": f"Error placing batch orders: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

