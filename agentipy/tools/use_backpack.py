from backpack_exchange_sdk.authenticated import AuthenticationClient
from backpack_exchange_sdk.public import PublicClient

from agentipy.agent import SolanaAgentKit


class BackpackManager:
    # BASE_URL = "https://api.backpack.exchange"
    def __init__(self, agent:SolanaAgentKit):
        """
        Initialize the BackpackManager with API key and secret.

        Args:
            api_key (str): Your API key for Backpack Exchange.
            api_secret (str): Your API secret for Backpack Exchange.
        """
        self.auth_client = AuthenticationClient(agent.backpack_api_key, agent.backpack_api_secret)
        self.public_client = PublicClient()

    # Authenticated API
    def get_account_balances(self) -> dict:
        """
        Retrieve the account balances.

        Returns:
            dict: The balances of the account.
        """
        try:
            balances = self.auth_client.get_balances()
            return balances
        except Exception as e:
            raise Exception(f"Error fetching account balances: {str(e)}")

    def request_withdrawal(
        self,
        address: str,
        blockchain: str,
        quantity: str,
        symbol: str,
        client_id: str = None,
        two_factor_token: str = None,
        auto_borrow: bool = None,
        auto_lend_redeem: bool = None,
    ) -> dict:
        """
        Request a withdrawal from the exchange.

        Args:
            address (str): Withdrawal destination address.
            blockchain (str): Blockchain name.
            quantity (str): Amount to withdraw.
            symbol (str): Asset symbol.
            client_id (str, optional): Client-specific identifier.
            two_factor_token (str, optional): Two-factor authentication token.
            auto_borrow (bool, optional): Enable auto-borrow.
            auto_lend_redeem (bool, optional): Enable auto-lend redemption.

        Returns:
            dict: Withdrawal request response.
        """
        try:
            return self.auth_client.request_withdrawal(
                address, blockchain, quantity, symbol, client_id, two_factor_token, auto_borrow, auto_lend_redeem
            )
        except Exception as e:
            raise Exception(f"Error requesting withdrawal: {str(e)}")

    def get_account_settings(self) -> dict:
        """
        Retrieve the account settings.

        Returns:
            dict: Account settings information.
        """
        try:
            settings = self.auth_client.get_account()
            return settings
        except Exception as e:
            raise Exception(f"Error fetching account settings: {str(e)}")

    def update_account_settings(
        self,
        auto_borrow_settlements: bool = None,
        auto_lend: bool = None,
        auto_realize_pnl: bool = None,
        auto_repay_borrows: bool = None,
        leverage_limit: str = None,
    ) -> None:
        """
        Update account settings.

        Args:
            auto_borrow_settlements (bool): Enable or disable auto borrow settlements.
            auto_lend (bool): Enable or disable auto lend.
            auto_realize_pnl (bool): Enable or disable auto realization of PNL.
            auto_repay_borrows (bool): Enable or disable auto repayment of borrows.
            leverage_limit (str): Set the leverage limit.
        """
        try:
            self.auth_client.update_account(
                autoBorrowSettlements=auto_borrow_settlements,
                autoLend=auto_lend,
                autoRealizePnl=auto_realize_pnl,
                autoRepayBorrows=auto_repay_borrows,
                leverageLimit=leverage_limit,
            )
        except Exception as e:
            raise Exception(f"Error updating account settings: {str(e)}")

    def get_borrow_lend_positions(self) -> dict:
        """
        Retrieve all open borrow/lend positions.

        Returns:
            dict: Borrow/lend positions.
        """
        try:
            positions = self.auth_client.get_borrow_lend_positions()
            return positions
        except Exception as e:
            raise Exception(f"Error fetching borrow/lend positions: {str(e)}")

    def execute_borrow_lend(self, quantity: str, side: str, symbol: str) -> None:
        """
        Execute a borrow or lend operation.

        Args:
            quantity (str): The quantity to borrow or lend.
            side (str): The operation side ('borrow' or 'lend').
            symbol (str): The asset symbol.
        """
        try:
            self.auth_client.execute_borrow_lend(quantity, side, symbol)
        except Exception as e:
            raise Exception(f"Error executing borrow/lend operation: {str(e)}")

    def get_collateral_info(self, sub_account_id: int = None) -> dict:
        """
        Retrieve collateral information.

        Args:
            sub_account_id (int, optional): Sub-account ID.

        Returns:
            dict: Collateral information.
        """
        try:
            collateral = self.auth_client.get_collateral(subAccountId=sub_account_id)
            return collateral
        except Exception as e:
            raise Exception(f"Error fetching collateral information: {str(e)}")
        
    def get_account_deposits(self, fromTimestamp: int = None, toTimestamp: int = None, limit: int = 100, offset: int = 0) -> dict:
        """
        Retrieves deposit history.

        Args:
            fromTimestamp (int, optional): starting timestamp
            toTimestamp (int, optional): ending timestamp
            limit (int, optional): number of deposits to return
            offset (int, optional): offset for pagination

        Returns:
            dict: deposit information of an account
        """
        try:
            deposits = self.auth_client.get_deposits(fromTimestamp=fromTimestamp, toTimestamp=toTimestamp, limit=limit, offset=offset)
            return deposits
        except Exception as e:
            raise Exception(f"Error fetching collateral information: {str(e)}")
    
    def get_open_positions(self) -> dict:
        """
        Retrieve account position summary.

        Returns:
            dict: Open positions.
        """
        try:
            return self.auth_client.get_open_positions()
        except Exception as e:
            raise Exception(f"Error fetching open positions: {str(e)}")

    def get_borrow_history(self, type: str = None, sources: str = None, position_id: str = None, symbol: str = None, limit: int = 100, offset: int = 0) -> dict:
        """
        Retrieve the history of borrow and lend operations.

        Args:
            type (str, optional): Filter by type.
            sources (str, optional): Filter by sources.
            position_id (str, optional): Filter by position ID.
            symbol (str, optional): Filter by asset symbol.
            limit (int, optional): Maximum results to return.
            offset (int, optional): Records to skip.

        Returns:
            dict: Borrow and lend history.
        """
        try:
            return self.auth_client.get_borrow_history(type, sources, position_id, symbol, limit, offset)
        except Exception as e:
            raise Exception(f"Error fetching borrow history: {str(e)}")

    def get_interest_history(self, symbol: str = None, position_id: str = None, limit: int = 100, offset: int = 0, sources: str = None) -> dict:
        """
        Retrieve interest payment history.

        Args:
            symbol (str, optional): Filter by asset symbol.
            position_id (str, optional): Filter by position ID.
            limit (int, optional): Maximum results to return.
            offset (int, optional): Records to skip.
            sources (str, optional): Filter by sources.

        Returns:
            dict: Interest payment history.
        """
        try:
            return self.auth_client.get_interest_history(symbol, position_id, limit, offset, sources)
        except Exception as e:
            raise Exception(f"Error fetching interest history: {str(e)}")

    def get_fill_history(self, order_id: str = None, from_timestamp: int = None, to_timestamp: int = None, symbol: str = None, limit: int = 100, offset: int = 0, fill_type: str = None) -> dict:
        """
        Retrieve historical fills with optional filters.

        Args:
            order_id (str, optional): Filter by order ID.
            from_timestamp (int, optional): Start timestamp for filtering.
            to_timestamp (int, optional): End timestamp for filtering.
            symbol (str, optional): Filter by asset symbol.
            limit (int, optional): Maximum results to return.
            offset (int, optional): Records to skip.
            fill_type (str, optional): Filter by fill type.

        Returns:
            dict: Fill history.
        """
        try:
            return self.auth_client.get_fill_history(order_id, from_timestamp, to_timestamp, symbol, limit, offset, fill_type)
        except Exception as e:
            raise Exception(f"Error fetching fill history: {str(e)}")
    def get_borrow_position_history(self, symbol: str = None, side: str = None, state: str = None, limit: int = 100, offset: int = 0) -> dict:
        """
        Retrieve the history of borrow and lend positions for the account.
        """
        try:
            return self.auth_client.get_borrow_position_history(
                symbol=symbol, side=side, state=state, limit=limit, offset=offset
            )
        except Exception as e:
            raise Exception(f"Error fetching borrow position history: {str(e)}")

    def get_funding_payments(self, subaccount_id: int = None, symbol: str = None, limit: int = 100, offset: int = 0) -> dict:
        """
        Retrieve funding payment history for futures.
        """
        try:
            return self.auth_client.get_funding_payments(
                subaccountId=subaccount_id, symbol=symbol, limit=limit, offset=offset
            )
        except Exception as e:
            raise Exception(f"Error fetching funding payments: {str(e)}")

    def get_order_history(self, order_id: str = None, symbol: str = None, limit: int = 100, offset: int = 0) -> dict:
        """
        Retrieve the order history for the user.
        """
        try:
            return self.auth_client.get_order_history(
                orderId=order_id, symbol=symbol, limit=limit, offset=offset
            )
        except Exception as e:
            raise Exception(f"Error fetching order history: {str(e)}")

    def get_pnl_history(self, subaccount_id: int = None, symbol: str = None, limit: int = 100, offset: int = 0) -> dict:
        """
        Retrieve the history of profit and loss realization for an account.
        """
        try:
            return self.auth_client.get_pnl_history(
                subaccountId=subaccount_id, symbol=symbol, limit=limit, offset=offset
            )
        except Exception as e:
            raise Exception(f"Error fetching PNL history: {str(e)}")

    def get_settlement_history(self, limit: int = 100, offset: int = 0, source: str = None) -> dict:
        """
        Retrieve the history of settlement operations for the account.
        """
        try:
            return self.auth_client.get_settlement_history(
                limit=limit, offset=offset, source=source
            )
        except Exception as e:
            raise Exception(f"Error fetching settlement history: {str(e)}")

    def get_users_open_orders(self, symbol: str, client_id: int = None, order_id: str = None) -> dict:
        """
        Retrieve an open order from the order book.
        """
        try:
            return self.auth_client.get_users_open_orders(
                symbol=symbol, clientId=client_id, orderId=order_id
            )
        except Exception as e:
            raise Exception(f"Error fetching user's open orders: {str(e)}")

    def execute_order(
        self,
        order_type: str,
        side: str,
        symbol: str,
        post_only: bool = False,
        client_id: int = None,
        price: str = None,
        quantity: str = None,
        time_in_force: str = None,
        quote_quantity: str = None,
        self_trade_prevention: str = None,
        trigger_price: str = None,
        reduce_only: bool = None,
        auto_borrow: bool = None,
        auto_borrow_repay: bool = None,
        auto_lend: bool = None,
        auto_lend_redeem: bool = None,
    ) -> dict:
        """
        Execute an order on the order book.
        """
        try:
            return self.auth_client.execute_order(
                orderType=order_type,
                side=side,
                symbol=symbol,
                postOnly=post_only,
                clientId=client_id,
                price=price,
                quantity=quantity,
                timeInForce=time_in_force,
                quoteQuantity=quote_quantity,
                selfTradePrevention=self_trade_prevention,
                triggerPrice=trigger_price,
                reduceOnly=reduce_only,
                autoBorrow=auto_borrow,
                autoBorrowRepay=auto_borrow_repay,
                autoLend=auto_lend,
                autoLendRedeem=auto_lend_redeem,
            )
        except Exception as e:
            raise Exception(f"Error executing order: {str(e)}")

    def cancel_open_order(self, symbol: str, client_id: int = None, order_id: str = None) -> dict:
        """
        Cancel an open order from the order book.
        """
        try:
            return self.auth_client.cancel_open_order(
                symbol=symbol, clientId=client_id, orderId=order_id
            )
        except Exception as e:
            raise Exception(f"Error canceling open order: {str(e)}")

    def get_open_orders(self, symbol: str = None) -> dict:
        """
        Retrieve all open orders for a user.
        """
        try:
            return self.auth_client.get_open_orders(symbol=symbol)
        except Exception as e:
            raise Exception(f"Error fetching open orders: {str(e)}")

    def cancel_open_orders(self, symbol: str) -> dict:
        """
        Cancel all open orders for a specific market.
        """
        try:
            return self.auth_client.cancel_open_orders(symbol=symbol)
        except Exception as e:
            raise Exception(f"Error canceling open orders: {str(e)}")
        
    # Public API
    def get_supported_assets(self) -> dict:
        """
        Get all supported assets.

        Returns:
            dict: A list of supported assets.
        """
        try:
            assets = self.public_client.get_assets()
            return assets
        except Exception as e:
            raise Exception(f"Error fetching supported assets: {str(e)}")

    def get_ticker_information(self, symbol: str) -> dict:
        """
        Get ticker information for a specific symbol.

        Args:
            symbol (str): The symbol to fetch ticker information for.

        Returns:
            dict: Ticker information for the specified symbol.
        """
        try:
            ticker = self.public_client.get_ticker(symbol)
            return ticker
        except Exception as e:
            raise Exception(f"Error fetching ticker information: {str(e)}")
        
    def get_collateral(self) -> dict:
        """
        Get collateral parameters for assets.

        Returns:
            dict: Collateral parameters.
        """
        try:
            return self.auth_client.get_collateral()
        except Exception as e:
            raise Exception(f"Error fetching collateral: {str(e)}")

    # ================================================================
    # Market - Public market data.
    # ================================================================

    def get_markets(self) -> dict:
        """
        Retrieves all the markets that are supported by the exchange.

        Returns:
            dict: Supported markets.
        """
        try:
            return self.public_client.get_markets()
        except Exception as e:
            raise Exception(f"Error fetching markets: {str(e)}")

    def get_market(self, symbol: str) -> dict:
        """
        Retrieves details for a specific market.

        Args:
            symbol (str): Market symbol.

        Returns:
            dict: Market details.
        """
        try:
            return self.public_client.get_market(symbol)
        except Exception as e:
            raise Exception(f"Error fetching market details: {str(e)}")

    def get_tickers(self) -> dict:
        """
        Retrieves summarized statistics for the last 24 hours for all market symbols.

        Returns:
            dict: Market tickers.
        """
        try:
            return self.public_client.get_tickers()
        except Exception as e:
            raise Exception(f"Error fetching tickers: {str(e)}")

    def get_depth(self, symbol: str) -> dict:
        """
        Retrieves the order book depth for a given market symbol.

        Args:
            symbol (str): Market symbol.

        Returns:
            dict: Order book depth.
        """
        try:
            return self.public_client.get_depth(symbol)
        except Exception as e:
            raise Exception(f"Error fetching depth: {str(e)}")

    def get_klines(self, symbol: str, interval: str, start_time: int, end_time: int = None) -> dict:
        """
        Get K-Lines for the given market symbol.

        Args:
            symbol (str): Market symbol.
            interval (str): Interval for the K-Lines.
            start_time (int): Start time for the data.
            end_time (int, optional): End time for the data. Defaults to None.

        Returns:
            dict: K-Lines data.
        """
        try:
            return self.public_client.get_klines(symbol, interval, start_time, end_time)
        except Exception as e:
            raise Exception(f"Error fetching K-Lines: {str(e)}")

    def get_mark_price(self, symbol: str) -> dict:
        """
        Retrieves mark price, index price, and funding rate for the given market symbol.

        Args:
            symbol (str): Market symbol.

        Returns:
            dict: Mark price data.
        """
        try:
            return self.public_client.get_mark_price(symbol)
        except Exception as e:
            raise Exception(f"Error fetching mark price: {str(e)}")

    def get_open_interest(self, symbol: str) -> dict:
        """
        Retrieves the current open interest for the given market.

        Args:
            symbol (str): Market symbol.

        Returns:
            dict: Open interest data.
        """
        try:
            return self.public_client.get_open_interest(symbol)
        except Exception as e:
            raise Exception(f"Error fetching open interest: {str(e)}")

    def get_funding_interval_rates(self, symbol: str, limit: int = 100, offset: int = 0) -> dict:
        """
        Funding interval rate history for futures.

        Args:
            symbol (str): Market symbol.
            limit (int, optional): Maximum results to return. Defaults to 100.
            offset (int, optional): Records to skip. Defaults to 0.

        Returns:
            dict: Funding interval rate data.
        """
        try:
            return self.public_client.get_funding_interval_rates(symbol, limit, offset)
        except Exception as e:
            raise Exception(f"Error fetching funding interval rates: {str(e)}")

    # ================================================================
    # System - Exchange system status.
    # ================================================================

    def get_status(self) -> dict:
        """
        Get the system status and the status message, if any.

        Returns:
            dict: System status.
        """
        try:
            return self.public_client.get_status()
        except Exception as e:
            raise Exception(f"Error fetching system status: {str(e)}")

    def send_ping(self) -> str:
        """
        Responds with pong.

        Returns:
            str: "pong"
        """
        try:
            return self.public_client.send_ping()
        except Exception as e:
            raise Exception(f"Error sending ping: {str(e)}")

    def get_system_time(self) -> str:
        """
        Retrieves the current system time.

        Returns:
            str: Current system time.
        """
        try:
            return self.public_client.get_system_time()
        except Exception as e:
            raise Exception(f"Error fetching system time: {str(e)}")

    # ================================================================
    # Trades - Public trade data.
    # ================================================================

    def get_recent_trades(self, symbol: str, limit: int = 100) -> dict:
        """
        Retrieve the most recent trades for a symbol.

        Args:
            symbol (str): Market symbol.
            limit (int, optional): Maximum results to return. Defaults to 100.

        Returns:
            dict: Recent trade data.
        """
        try:
            return self.public_client.get_recent_trades(symbol, limit)
        except Exception as e:
            raise Exception(f"Error fetching recent trades: {str(e)}")

    def get_historical_trades(self, symbol: str, limit: int = 100, offset: int = 0) -> dict:
        """
        Retrieves all historical trades for the given symbol.

        Args:
            symbol (str): Market symbol.
            limit (int, optional): Maximum results to return. Defaults to 100.
            offset (int, optional): Records to skip. Defaults to 0.

        Returns:
            dict: Historical trade data.
        """
        try:
            return self.public_client.get_historical_trades(symbol, limit, offset)
        except Exception as e:
            raise Exception(f"Error fetching historical trades: {str(e)}")