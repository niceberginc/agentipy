import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool

from agentipy.helpers import validate_input

class ClosePerpTradeShortTool(BaseTool):
    name: str = "close_perp_trade_short"
    description: str = """
    Closes a perpetual short trade.

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
            
            transaction = await self.solana_kit.close_perp_trade_short(
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
                "message": f"Error closing perp short trade: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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

class OpenPerpTradeLongTool(BaseTool):
    name: str = "open_perp_trade_long"
    description: str = """
    Opens a perpetual long trade.

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
            
            
           
            transaction = await self.solana_kit.open_perp_trade_long(
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
                "message": f"Error opening perp long trade: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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
 

def get_perp_tools(solana_kit: SolanaAgentKit):
    return [
        ClosePerpTradeShortTool(solana_kit=solana_kit),
        ClosePerpTradeLongTool(solana_kit=solana_kit),
        OpenPerpTradeLongTool(solana_kit=solana_kit),
        OpenPerpTradeShortTool(solana_kit=solana_kit)
    ]

