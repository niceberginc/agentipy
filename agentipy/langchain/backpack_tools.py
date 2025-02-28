import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool

from agentipy.helpers import validate_input

class BackpackGetAccountBalancesTool(BaseTool):
    name: str = "backpack_get_account_balances"
    description: str = """
    Fetches account balances using the BackpackManager.

    Input: None
    Output:
    {
        "balances": "dict, the account balances",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            balances = await self.solana_kit.get_account_balances()
            return {
                "balances": balances,
                "message": "Success"
            }
        except Exception as e:
            return {
                "balances": None,
                "message": f"Error fetching account balances: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackRequestWithdrawalTool(BaseTool):
    name: str = "backpack_request_withdrawal"
    description: str = """
    Requests a withdrawal using the BackpackManager.

    Input: A JSON string with:
    {
        "address": "string, the destination address",
        "blockchain": "string, the blockchain name",
        "quantity": "string, the quantity to withdraw",
        "symbol": "string, the token symbol",
        "additional_params": "optional additional parameters as JSON object"
    }
    Output:
    {
        "result": "dict, the withdrawal request result",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "address": {"type": str, "required": True},
                "blockchain": {"type": str, "required": True},
                "quantity": {"type": str, "required": True},
                "symbol": {"type": str, "required": True},
                "additional_params": {"type": dict, "required": False}
            }
            validate_input(data, schema)

            result = await self.solana_kit.request_withdrawal(
                address=data["address"],
                blockchain=data["blockchain"],
                quantity=data["quantity"],
                symbol=data["symbol"],
                **data.get("additional_params", {})
            )
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error requesting withdrawal: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetAccountSettingsTool(BaseTool):
    name: str = "backpack_get_account_settings"
    description: str = """
    Fetches account settings using the BackpackManager.

    Input: None
    Output:
    {
        "settings": "dict, the account settings",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            settings = await self.solana_kit.get_account_settings()
            return {
                "settings": settings,
                "message": "Success"
            }
        except Exception as e:
            return {
                "settings": None,
                "message": f"Error fetching account settings: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackUpdateAccountSettingsTool(BaseTool):
    name: str = "backpack_update_account_settings"
    description: str = """
    Updates account settings using the BackpackManager.

    Input: A JSON string with additional parameters for the account settings.
    Output:
    {
        "result": "dict, the result of the update",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.update_account_settings(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error updating account settings: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetBorrowLendPositionsTool(BaseTool):
    name: str = "backpack_get_borrow_lend_positions"
    description: str = """
    Fetches borrow/lend positions using the BackpackManager.

    Input: None
    Output:
    {
        "positions": "list, the borrow/lend positions",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            positions = await self.solana_kit.get_borrow_lend_positions()
            return {
                "positions": positions,
                "message": "Success"
            }
        except Exception as e:
            return {
                "positions": None,
                "message": f"Error fetching borrow/lend positions: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackExecuteBorrowLendTool(BaseTool):
    name: str = "backpack_execute_borrow_lend"
    description: str = """
    Executes a borrow/lend operation using the BackpackManager.

    Input: A JSON string with:
    {
        "quantity": "string, the amount to borrow or lend",
        "side": "string, either 'borrow' or 'lend'",
        "symbol": "string, the token symbol"
    }
    Output:
    {
        "result": "dict, the result of the operation",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "quantity": {"type": str, "required": True},
                "side": {"type": str, "required": True},
                "symbol": {"type": str, "required": True}
            }
            validate_input(data, schema)

            result = await self.solana_kit.execute_borrow_lend(
                quantity=data["quantity"],
                side=data["side"],
                symbol=data["symbol"]
            )
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error executing borrow/lend operation: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetFillHistoryTool(BaseTool):
    name: str = "backpack_get_fill_history"
    description: str = """
    Fetches the fill history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the fill history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_fill_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching fill history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetBorrowPositionHistoryTool(BaseTool):
    name: str = "backpack_get_borrow_position_history"
    description: str = """
    Fetches the borrow position history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the borrow position history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_borrow_position_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching borrow position history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetFundingPaymentsTool(BaseTool):
    name: str = "backpack_get_funding_payments"
    description: str = """
    Fetches funding payments using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "payments": "list, the funding payments records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            payments = await self.solana_kit.get_funding_payments(**data)
            return {
                "payments": payments,
                "message": "Success"
            }
        except Exception as e:
            return {
                "payments": None,
                "message": f"Error fetching funding payments: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetOrderHistoryTool(BaseTool):
    name: str = "backpack_get_order_history"
    description: str = """
    Fetches order history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the order history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_order_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching order history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetPnlHistoryTool(BaseTool):
    name: str = "backpack_get_pnl_history"
    description: str = """
    Fetches PNL history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the PNL history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_pnl_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching PNL history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetSettlementHistoryTool(BaseTool):
    name: str = "backpack_get_settlement_history"
    description: str = """
    Fetches settlement history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the settlement history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_settlement_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching settlement history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetUsersOpenOrdersTool(BaseTool):
    name: str = "backpack_get_users_open_orders"
    description: str = """
    Fetches user's open orders using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "open_orders": "list, the user's open orders",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            open_orders = await self.solana_kit.get_users_open_orders(**data)
            return {
                "open_orders": open_orders,
                "message": "Success"
            }
        except Exception as e:
            return {
                "open_orders": None,
                "message": f"Error fetching user's open orders: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackExecuteOrderTool(BaseTool):
    name: str = "backpack_execute_order"
    description: str = """
    Executes an order using the BackpackManager.

    Input: A JSON string with order parameters.
    Output:
    {
        "result": "dict, the execution result",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.execute_order(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error executing order: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackCancelOpenOrderTool(BaseTool):
    name: str = "backpack_cancel_open_order"
    description: str = """
    Cancels an open order using the BackpackManager.

    Input: A JSON string with order details.
    Output:
    {
        "result": "dict, the cancellation result",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.cancel_open_order(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error canceling open order: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetOpenOrdersTool(BaseTool):
    name: str = "backpack_get_open_orders"
    description: str = """
    Fetches open orders using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "open_orders": "list, the open orders",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            open_orders = await self.solana_kit.get_open_orders(**data)
            return {
                "open_orders": open_orders,
                "message": "Success"
            }
        except Exception as e:
            return {
                "open_orders": None,
                "message": f"Error fetching open orders: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackCancelOpenOrdersTool(BaseTool):
    name: str = "backpack_cancel_open_orders"
    description: str = """
    Cancels multiple open orders using the BackpackManager.

    Input: A JSON string with order details.
    Output:
    {
        "result": "dict, the cancellation result",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.cancel_open_orders(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error canceling open orders: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetSupportedAssetsTool(BaseTool):
    name: str = "backpack_get_supported_assets"
    description: str = """
    Fetches supported assets using the BackpackManager.

    Input: None
    Output:
    {
        "assets": "list, the supported assets",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            assets = await self.solana_kit.get_supported_assets()
            return {
                "assets": assets,
                "message": "Success"
            }
        except Exception as e:
            return {
                "assets": None,
                "message": f"Error fetching supported assets: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetTickerInformationTool(BaseTool):
    name: str = "backpack_get_ticker_information"
    description: str = """
    Fetches ticker information using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "ticker_information": "dict, the ticker information",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            ticker_info = await self.solana_kit.get_ticker_information(**data)
            return {
                "ticker_information": ticker_info,
                "message": "Success"
            }
        except Exception as e:
            return {
                "ticker_information": None,
                "message": f"Error fetching ticker information: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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

class BackpackGetStatusTool(BaseTool):
    name: str = "backpack_get_status"
    description: str = """
    Fetches the system status and any status messages using the BackpackManager.

    Input: None
    Output:
    {
        "status": "dict, the system status",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            status = await self.solana_kit.get_status()
            return {
                "status": status,
                "message": "Success"
            }
        except Exception as e:
            return {
                "status": None,
                "message": f"Error fetching system status: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackSendPingTool(BaseTool):
    name: str = "backpack_send_ping"
    description: str = """
    Sends a ping and expects a "pong" response using the BackpackManager.

    Input: None
    Output:
    {
        "response": "string, the response ('pong')",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            response = await self.solana_kit.send_ping()
            return {
                "response": response,
                "message": "Success"
            }
        except Exception as e:
            return {
                "response": None,
                "message": f"Error sending ping: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetSystemTimeTool(BaseTool):
    name: str = "backpack_get_system_time"
    description: str = """
    Fetches the current system time using the BackpackManager.

    Input: None
    Output:
    {
        "system_time": "string, the current system time",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            system_time = await self.solana_kit.get_system_time()
            return {
                "system_time": system_time,
                "message": "Success"
            }
        except Exception as e:
            return {
                "system_time": None,
                "message": f"Error fetching system time: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetRecentTradesTool(BaseTool):
    name: str = "backpack_get_recent_trades"
    description: str = """
    Fetches the most recent trades for a given market symbol using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol",
        "limit": "int, optional, maximum results to return (default: 100)"
    }
    Output:
    {
        "recent_trades": "dict, the recent trade data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "symbol": {"type": str, "required": True},
                "limit": {"type": int, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)

            symbol = data["symbol"]
            limit = data.get("limit", 100)

            recent_trades = await self.solana_kit.get_recent_trades(
                symbol=symbol,
                limit=limit
            )
            return {
                "recent_trades": recent_trades,
                "message": "Success"
            }
        except Exception as e:
            return {
                "recent_trades": None,
                "message": f"Error fetching recent trades: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetHistoricalTradesTool(BaseTool):
    name: str = "backpack_get_historical_trades"
    description: str = """
    Fetches historical trades for a given market symbol using the BackpackManager.

    Input: A JSON string with:
    {
        "symbol": "string, the market symbol",
        "limit": "int, optional, maximum results to return (default: 100)",
        "offset": "int, optional, records to skip (default: 0)"
    }
    Output:
    {
        "historical_trades": "dict, the historical trade data",
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

            historical_trades = await self.solana_kit.get_historical_trades(
                symbol=symbol,
                limit=limit,
                offset=offset
            )
            return {
                "historical_trades": historical_trades,
                "message": "Success"
            }
        except Exception as e:
            return {
                "historical_trades": None,
                "message": f"Error fetching historical trades: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetCollateralInfoTool(BaseTool):
    name: str = "backpack_get_collateral_info"
    description: str = """
    Fetches collateral information using the BackpackManager.

    Input: A JSON string with:
    {
        "sub_account_id": "int, optional, the sub-account ID for collateral information"
    }
    Output:
    {
        "collateral_info": "dict, the collateral information",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "sub_account_id": {"type": int, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)

            collateral_info = await self.solana_kit.get_collateral_info(
                sub_account_id=data.get("sub_account_id")
            )
            return {
                "collateral_info": collateral_info,
                "message": "Success"
            }
        except Exception as e:
            return {
                "collateral_info": None,
                "message": f"Error fetching collateral information: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetAccountDepositsTool(BaseTool):
    name: str = "backpack_get_account_deposits"
    description: str = """
    Fetches account deposits using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "deposits": "dict, the account deposit data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "sub_account_id": {"type": int, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)

            sub_account_id = data.get("sub_account_id")
            deposits = await self.solana_kit.get_account_deposits(
                sub_account_id=sub_account_id
            )
            return {
                "deposits": deposits,
                "message": "Success"
            }
        except Exception as e:
            return {
                "deposits": None,
                "message": f"Error fetching account deposits: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetOpenPositionsTool(BaseTool):
    name: str = "backpack_get_open_positions"
    description: str = """
    Fetches open positions using the BackpackManager.

    Input: None
    Output:
    {
        "open_positions": "list, the open positions",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            open_positions = await self.solana_kit.get_open_positions()
            return {
                "open_positions": open_positions,
                "message": "Success"
            }
        except Exception as e:
            return {
                "open_positions": None,
                "message": f"Error fetching open positions: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetBorrowHistoryTool(BaseTool):
    name: str = "backpack_get_borrow_history"
    description: str = """
    Fetches borrow history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "borrow_history": "list, the borrow history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            borrow_history = await self.solana_kit.get_borrow_history(**data)
            return {
                "borrow_history": borrow_history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "borrow_history": None,
                "message": f"Error fetching borrow history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetInterestHistoryTool(BaseTool):
    name: str = "backpack_get_interest_history"
    description: str = """
    Fetches interest history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "interest_history": "list, the interest history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            interest_history = await self.solana_kit.get_interest_history(**data)
            return {
                "interest_history": interest_history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "interest_history": None,
                "message": f"Error fetching interest history: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


def get_backpack_tools(solana_kit: SolanaAgentKit):
    return [
        BackpackGetTickersTool(solana_kit=solana_kit),
        BackpackGetDepthTool(solana_kit=solana_kit),
        BackpackGetKlinesTool(solana_kit=solana_kit),
        BackpackGetMarkPriceTool(solana_kit=solana_kit),
        BackpackGetOpenInterestTool(solana_kit=solana_kit),
        BackpackGetFundingIntervalRatesTool(solana_kit=solana_kit),
        BackpackGetStatusTool(solana_kit=solana_kit),
        BackpackSendPingTool(solana_kit=solana_kit),
        BackpackGetSystemTimeTool(solana_kit=solana_kit),
        BackpackGetRecentTradesTool(solana_kit=solana_kit),
        BackpackGetHistoricalTradesTool(solana_kit=solana_kit),
        BackpackGetCollateralInfoTool(solana_kit=solana_kit),
        BackpackGetAccountDepositsTool(solana_kit=solana_kit),
        BackpackGetOpenPositionsTool(solana_kit=solana_kit),
        BackpackGetBorrowHistoryTool(solana_kit=solana_kit),
        BackpackGetInterestHistoryTool(solana_kit=solana_kit),
       
    ]
