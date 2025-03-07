import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class BackpackGetMarketsTool(BaseTool):
    name: str = "backpack_get_markets"
    description: str = """
    Fetches all markets using the BackpackManager.

    Input: None
    Output:
    {
        "markets": "list, the available markets",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            markets = await self.solana_kit.get_markets()
            return {
                "markets": markets,
                "message": "Success"
            }
        except Exception as e:
            return {
                "markets": None,
                "message": f"Error fetching markets: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetMarketTool(BaseTool):
    name: str = "backpack_get_market"
    description: str = """
    Fetches a specific market using the BackpackManager.

    Input: A JSON string with market query parameters.
    Output:
    {
        "market": "dict, the market data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            market = await self.solana_kit.get_market(**data)
            return {
                "market": market,
                "message": "Success"
            }
        except Exception as e:
            return {
                "market": None,
                "message": f"Error fetching market: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetTickersTool(BaseTool):
    name: str = "backpack_get_tickers"
    description: str = """
    Fetches tickers for all markets using the BackpackManager.

    Input: None
    Output:
    {
        "tickers": "list, the market tickers",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            tickers = await self.solana_kit.get_tickers()
            return {
                "tickers": tickers,
                "message": "Success"
            }
        except Exception as e:
            return {
                "tickers": None,
                "message": f"Error fetching tickers: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetDepthTool(BaseTool):
    name: str = "backpack_get_depth"
    description: str = """
    Fetches the order book depth for a given market symbol using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol"
    }
    Output:
    {
        "depth": "dict, the order book depth",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "symbol": {"type": str, "required": True}
            }
            validate_input(data, schema)

            symbol = data["symbol"]
            depth = await self.solana_kit.get_depth(symbol)
            return {
                "depth": depth,
                "message": "Success"
            }
        except Exception as e:
            return {
                "depth": None,
                "message": f"Error fetching depth: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetKlinesTool(BaseTool):
    name: str = "backpack_get_klines"
    description: str = """
    Fetches K-Lines data for a given market symbol using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol",
        "interval": "string, the interval for K-Lines",
        "start_time": "int, the start time for data",
        "end_time": "int, optional, the end time for data"
    }
    Output:
    {
        "klines": "dict, the K-Lines data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "symbol": {"type": str, "required": True},
                "interval": {"type": str, "required": True},
                "start_time": {"type": int, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)

            klines = await self.solana_kit.get_klines(
                symbol=data["symbol"],
                interval=data["interval"],
                start_time=data["start_time"],
                end_time=data.get("end_time")
            )
            return {
                "klines": klines,
                "message": "Success"
            }
        except Exception as e:
            return {
                "klines": None,
                "message": f"Error fetching K-Lines: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetMarkPriceTool(BaseTool):
    name: str = "backpack_get_mark_price"
    description: str = """
    Fetches mark price, index price, and funding rate for a given market symbol.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol"
    }
    Output:
    {
        "mark_price_data": "dict, the mark price data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "symbol": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)

            symbol = data["symbol"]
            mark_price_data = await self.solana_kit.get_mark_price(symbol)
            return {
                "mark_price_data": mark_price_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "mark_price_data": None,
                "message": f"Error fetching mark price: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetOpenInterestTool(BaseTool):
    name: str = "backpack_get_open_interest"
    description: str = """
    Fetches the open interest for a given market symbol using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol"
    }
    Output:
    {
        "open_interest": "dict, the open interest data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "symbol": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)

            symbol = data["symbol"]
            open_interest = await self.solana_kit.get_open_interest(symbol)
            return {
                "open_interest": open_interest,
                "message": "Success"
            }
        except Exception as e:
            return {
                "open_interest": None,
                "message": f"Error fetching open interest: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetFundingIntervalRatesTool(BaseTool):
    name: str = "backpack_get_funding_interval_rates"
    description: str = """
    Fetches funding interval rate history for futures using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol",
        "limit": "int, optional, maximum results to return (default: 100)",
        "offset": "int, optional, records to skip (default: 0)"
    }
    Output:
    {
        "funding_rates": "dict, the funding interval rate data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "symbol": {"type": str, "required": True},
                "limit": {"type": int, "required": False},
                "offset": {"type": int, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)

            symbol = data["symbol"]
            limit = data.get("limit", 100)
            offset = data.get("offset", 0)

            funding_rates = await self.solana_kit.get_funding_interval_rates(
                symbol=symbol,
                limit=limit,
                offset=offset
            )
            return {
                "funding_rates": funding_rates,
                "message": "Success"
            }
        except Exception as e:
            return {
                "funding_rates": None,
                "message": f"Error fetching funding interval rates: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
