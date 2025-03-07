import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class GetAvailableDriftMarketsTool(BaseTool):
    name: str = "get_available_drift_markets"
    description: str = """
    Retrieves available markets on Drift.

    Input: None.
    Output:
    {
        "markets": "dict, list of available Drift markets",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            markets = await self.solana_kit.get_available_drift_markets()
            return {
                "markets": markets,
                "message": "Success"
            }
        except Exception as e:
            return {
                "markets": None,
                "message": f"Error fetching available Drift markets: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class TradeUsingDriftPerpAccountTool(BaseTool):
    name: str = "trade_using_drift_perp_account"
    description: str = """
    Executes a trade using a Drift perpetual account.

    Input: A JSON string with:
    {
        "amount": "float, trade amount",
        "symbol": "string, market symbol",
        "action": "string, 'long' or 'short'",
        "trade_type": "string, 'market' or 'limit'",
        "price": "float, optional, trade execution price"
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
                "amount": {"type": float, "required": True},
                "symbol": {"type": str, "required": True},
                "action": {"type": str, "required": True},
                "trade_type": {"type": str, "required": True},
                "price": {"type": float, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)
            transaction = await self.solana_kit.trade_using_drift_perp_account(
                amount=data["amount"],
                symbol=data["symbol"],
                action=data["action"],
                trade_type=data["trade_type"],
                price=data.get("price"),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error trading using Drift perp account: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class GetDriftPerpMarketFundingRateTool(BaseTool):
    name: str = "get_drift_perp_market_funding_rate"
    description: str = """
    Retrieves the funding rate for a Drift perpetual market.

    Input: A JSON string with:
    {
        "symbol": "string, market symbol (must end in '-PERP')",
        "period": "string, optional, funding rate period, either 'year' or 'hour' (default: 'year')"
    }
    Output:
    {
        "funding_rate": "dict, funding rate details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "symbol": {"type": str, "required": True},
                "period": {"type": str, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)            
            funding_rate = await self.solana_kit.get_drift_perp_market_funding_rate(
                symbol=data["symbol"],
                period=data.get("period", "year"),
            )
            return {
                "funding_rate": funding_rate,
                "message": "Success"
            }
        except Exception as e:
            return {
                "funding_rate": None,
                "message": f"Error getting Drift perp market funding rate: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class GetDriftEntryQuoteOfPerpTradeTool(BaseTool):
    name: str = "get_drift_entry_quote_of_perp_trade"
    description: str = """
    Retrieves the entry quote for a perpetual trade on Drift.

    Input: A JSON string with:
    {
        "amount": "float, trade amount",
        "symbol": "string, market symbol (must end in '-PERP')",
        "action": "string, 'long' or 'short'"
    }
    Output:
    {
        "entry_quote": "dict, entry quote details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "amount": {"type": float, "required": True},
                "symbol": {"type": str, "required": True},
                "action": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            entry_quote = await self.solana_kit.get_drift_entry_quote_of_perp_trade(
                amount=data["amount"],
                symbol=data["symbol"],
                action=data["action"],
            )
            return {
                "entry_quote": entry_quote,
                "message": "Success"
            }
        except Exception as e:
            return {
                "entry_quote": None,
                "message": f"Error getting Drift entry quote of perp trade: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class DriftSwapSpotTokenTool(BaseTool):
    name: str = "drift_swap_spot_token"
    description: str = """
    Swaps spot tokens on Drift.

    Input: A JSON string with:
    {
        "from_symbol": "string, token to swap from",
        "to_symbol": "string, token to swap to",
        "slippage": "float, optional, allowed slippage",
        "to_amount": "float, optional, desired amount of the output token",
        "from_amount": "float, optional, amount of the input token"
    }
    Output:
    {
        "transaction": "dict, swap transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "from_symbol": {"type": str, "required": True},
                "to_symbol": {"type": str, "required": True},
                "slippage": {"type": float, "required": False},
                "to_amount": {"type": float, "required": False},
                "from_amount": {"type": float, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)           
            transaction = await self.solana_kit.drift_swap_spot_token(
                from_symbol=data["from_symbol"],
                to_symbol=data["to_symbol"],
                slippage=data.get("slippage"),
                to_amount=data.get("to_amount"),
                from_amount=data.get("from_amount"),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error swapping spot token on Drift: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

