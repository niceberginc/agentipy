import logging
import os
from enum import Enum
from typing import Optional, Union

from allora_sdk.v2.api_client import (PriceInferenceTimeframe,
                                      PriceInferenceToken, SignatureFormat)
from eth_account import Account
from web3 import Web3

from agentipy.constants import API_VERSION, BASE_PROXY_URL
from agentipy.tools.evm.wallet_opts import Web3EVMClient
from agentipy.utils import AgentKitError
from agentipy.utils.evm.general.networks import Network
from agentipy.wallet.crossMint_wallet_client import CrossmintWalletClient
from agentipy.wallet.evm_wallet_client import EVMWalletClient
from agentipy.wallet.privy_wallet_client import ChainType, PrivyWalletClient

logger = logging.getLogger(__name__)


class WalletType(str, Enum):
    """Enum for wallet types"""

    PRIVATE_KEY = "private_key"
    CROSSMINT = "crossmint"
    PRIVY = "privy"


class EvmAgentKit:
    """
    Main class for interacting with multiple EVM blockchains.
    Supports token operations, contract interactions, and chain-specific functionality.

    Attributes:
        web3 (Web3): Web3 provider for interacting with the blockchain.
        wallet_address (str): Public address of the wallet.
        private_key (str): Private key for signing transactions.
        chain_id (int): Chain ID of the connected EVM network.
        token (str): Native token symbol of the network.
        explorer (str): Blockchain explorer URL.
    """

    def __init__(
        self,
        network: Network,
        wallet_type: Union[WalletType, str] = WalletType.PRIVATE_KEY,
        private_key: Optional[str] = None,
        rpc_url: Optional[str] = None,
        rpc_api_key: Optional[str] = None,
        crossmint_api_key: Optional[str] = None,
        crossmint_wallet_locator: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        coingecko_api_key: Optional[str] = None,
        coingecko_demo_api_key: Optional[str] = None,
        stork_api_key: Optional[str] = None,
        elfa_ai_api_key: Optional[str] = None,
        allora_api_key: Optional[str] = None,
        privy_app_id: Optional[str] = None,
        privy_app_secret: Optional[str] = None,
        privy_wallet_id: Optional[str] = None,
        generate_wallet: bool = False,
    ):
        self.network = network
        self.wallet_type = wallet_type
        self.rpc_url = rpc_url or os.getenv("EVM_RPC_URL", network.rpc)
        self.rpc_api_key = rpc_api_key or os.getenv("EVM_RPC_API_KEY", "")
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY", "")
        self.coingecko_api_key = coingecko_api_key or os.getenv(
            "COINGECKO_PRO_API_KEY", ""
        )
        self.coingecko_demo_api_key = coingecko_demo_api_key or os.getenv(
            "COINGECKO_DEMO_API_KEY", ""
        )
        self.stork_api_key = stork_api_key or os.getenv("STORK_API_KEY", "")
        self.elfa_ai_api_key = elfa_ai_api_key or os.getenv("ELFA_AI_API_KEY", "")
        self.allora_api_key = allora_api_key or os.getenv("ALLORA_API_KEY", "")
        self.chain_id = network.chain_id
        self.token = network.token
        self.explorer = network.explorer
        self.eip1559_support = network.eip1559_support
        self.base_proxy_url = BASE_PROXY_URL
        self.api_version = API_VERSION
        self.privy_app_id = privy_app_id
        self.privy_app_secret = privy_app_secret
        self.privy_wallet_id = privy_wallet_id

        if wallet_type == WalletType.PRIVY or wallet_type == "privy":
            if not self.privy_app_id or not self.privy_app_secret:
                raise ValueError(
                    "PRIVY_APP_ID and PRIVY_APP_SECRET must be provided to use Privy wallet."
                )

            self.wallet_client = PrivyWalletClient(
                self.web3,
                self.privy_app_id,
                self.privy_app_secret,
                chain_type=ChainType.EVM,
                chain_id=self.chain_id,
            )

            if generate_wallet:
                wallet_info = self.wallet_client.create_wallet()
                self.wallet_id = wallet_info["id"]
                self.wallet_address = Web3.to_checksum_address(wallet_info["address"])
                print("selfaddr:", self.wallet_address)
                print("selfid:", self.wallet_id)
            else:
                wallet_address = self.wallet_client.use_wallet(privy_wallet_id)
                self.wallet_address = Web3.to_checksum_address(wallet_address)
                self.wallet_id = privy_wallet_id
                print(self.wallet_address)
        elif wallet_type == WalletType.CROSSMINT or wallet_type == "crossmint":
            # Use Crossmint wallet
            self.crossmint_api_key = crossmint_api_key or os.getenv(
                "CROSSMINT_API_KEY", ""
            )
            if not self.crossmint_api_key:
                raise AgentKitError(
                    "A valid Crossmint API key must be provided when using Crossmint wallet."
                )

            # Initialize the Crossmint wallet client with locator
            self.wallet_client = CrossmintWalletClient(
                self.web3,
                self.crossmint_api_key,
                wallet_locator=crossmint_wallet_locator,
            )
            self.wallet_address = self.wallet_client.get_address()
            self.private_key = None  # No private key when using Crossmint

        else:  # Default to private key wallet
            # Handle private key wallet initialization
            if generate_wallet:
                self.private_key, self.wallet_address = self.generate_wallet()
            else:
                self.private_key = private_key or os.getenv("EVM_PRIVATE_KEY", "")
                if not self.private_key:
                    raise AgentKitError(
                        "A valid private key must be provided when using private key wallet."
                    )
                self.wallet_address = self.web3.eth.account.from_key(
                    self.private_key
                ).address

            self.wallet_client = EVMWalletClient(self.web3, self.private_key)

        logger.info(
            f"Connected to {network.name} (Chain ID: {self.chain_id}) - RPC: {self.rpc_url}"
        )
        logger.info(f"Wallet address: {self.wallet_address}")

    @staticmethod
    def generate_wallet():
        """
        Generates a new EVM wallet with a random private key.
        """
        account = Account.create()
        private_key = account.key.hex()
        wallet_address = account.address
        logger.info(f"New Wallet Generated: {wallet_address}")
        return private_key, wallet_address

    async def get_wallet_address(self) -> str:
        """
        Get the wallet's address.

        Returns:
            str: The wallet's address in string format.
        """
        return str(self.wallet_address)
    
    async def get_sentient_listings(
        self, page_number: Optional[int] = 1, page_size: Optional[int] = 30
    ):
        """
        Retrieves Sentient listings.

        Args:
            page_number (int, optional): The page number for paginated results (default: 1).
            page_size (int, optional): The number of items per page (default: 30).

        Returns:
            dict: Listings data or error details.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.get_sentient_listings(self, page_number, page_size)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch Sentient listings: {e}")

    async def buy_sentient(
        self, token_address: str, amount: str, builder_id: Optional[int] = None
    ):
        """
        Buys Sentient tokens.

        Args:
            token_address (str): The token address.
            amount (str): The amount to purchase.
            builder_id (int, optional): The builder ID for the purchase.

        Returns:
            dict: Transaction receipt or error details.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.buy_sentient(self, token_address, amount, builder_id)
        except Exception as e:
            raise AgentKitError(f"Failed to buy Sentient tokens: {e}")

    async def sell_sentient(
        self, token_address: str, amount: str, builder_id: Optional[int] = None
    ):
        """
        Sells Sentient tokens.

        Args:
            token_address (str): The token address.
            amount (str): The amount to sell.
            builder_id (int, optional): The builder ID for the sale.

        Returns:
            dict: Transaction receipt or error details.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.sell_sentient(
                self, token_address, amount, builder_id
            )
        except Exception as e:
            raise AgentKitError(f"Failed to sell Sentient tokens: {e}")

    async def buy_prototype(
        self,
        token_address: str,
        amount: str,
        builder_id: Optional[int] = None,
        slippage: Optional[float] = None,
    ):
        """
        Buys Prototype tokens.

        Args:
            token_address (str): The token address.
            amount (str): The amount to purchase.
            builder_id (int, optional): The builder ID for the purchase.
            slippage (float, optional): Slippage tolerance percentage.

        Returns:
            dict: Transaction receipt or error details.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.buy_prototype(
                self, token_address, amount, builder_id, slippage
            )
        except Exception as e:
            raise AgentKitError(f"Failed to buy Prototype tokens: {e}")

    async def sell_prototype(
        self,
        token_address: str,
        amount: str,
        builder_id: Optional[int] = None,
        slippage: Optional[float] = None,
    ):
        """
        Sells Prototype tokens.

        Args:
            token_address (str): The token address.
            amount (str): The amount to sell.
            builder_id (int, optional): The builder ID for the sale.
            slippage (float, optional): Slippage tolerance percentage.

        Returns:
            dict: Transaction receipt or error details.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.sell_prototype(
                self, token_address, amount, builder_id, slippage
            )
        except Exception as e:
            raise AgentKitError(f"Failed to sell Prototype tokens: {e}")

    async def check_sentient_allowance(
        self, amount: str, from_token_address: Optional[str] = None
    ):
        """
        Checks Sentient token allowance.

        Args:
            amount (str): The amount to check allowance for.
            from_token_address (str, optional): The address of the token being checked.

        Returns:
            dict: Boolean indicating whether allowance is sufficient.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.check_sentient_allowance(
                self, amount, from_token_address
            )
        except Exception as e:
            raise AgentKitError(f"Failed to check Sentient allowance: {e}")

    async def approve_sentient_allowance(
        self, amount: str, from_token_address: Optional[str] = None
    ):
        """
        Approves Sentient token allowance.

        Args:
            amount (str): The amount to approve.
            from_token_address (str, optional): The token address being approved.

        Returns:
            dict: Transaction hash or error details.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.approve_sentient_allowance(
                self, amount, from_token_address
            )
        except Exception as e:
            raise AgentKitError(f"Failed to approve Sentient allowance: {e}")

    async def check_prototype_allowance(
        self, amount: str, from_token_address: Optional[str] = None
    ):
        """
        Checks Prototype token allowance.

        Args:
            amount (str): The amount to check allowance for.
            from_token_address (str, optional): The address of the token being checked.

        Returns:
            dict: Boolean indicating whether allowance is sufficient.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.check_prototype_allowance(
                self, amount, from_token_address
            )
        except Exception as e:
            raise AgentKitError(f"Failed to check Prototype allowance: {e}")

    async def approve_prototype_allowance(
        self, amount: str, from_token_address: Optional[str] = None
    ):
        """
        Approves Prototype token allowance.

        Args:
            amount (str): The amount to approve.
            from_token_address (str, optional): The token address being approved.

        Returns:
            dict: Transaction hash or error details.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.approve_prototype_allowance(
                self, amount, from_token_address
            )
        except Exception as e:
            raise AgentKitError(f"Failed to approve Prototype allowance: {e}")

    async def get_prototype_listing(self, page_number: int = 1, page_size: int = 30):
        """
        Retrieves Prototype token listings.

        Args:
            page_number (int, optional): Page number for pagination.
            page_size (int, optional): Number of items per page.

        Returns:
            dict: List of Prototype token listings or error details.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.get_prototype_listing(self, page_number, page_size)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch Prototype listings: {e}")

    async def fetch_klines(
        self, token_address: str, granularity: int, start: int, end: int, limit: int
    ):
        """
        Fetches Klines (candlestick chart data) for a token.

        Args:
            token_address (str): The token address.
            granularity (int): The granularity of the data.
            start (int): The start timestamp.
            end (int): The end timestamp.
            limit (int): The number of data points.

        Returns:
            dict: Kline data or error details.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.fetch_klines(
                self, token_address, granularity, start, end, limit
            )
        except Exception as e:
            raise AgentKitError(f"Failed to fetch Klines: {e}")

    async def search_virtual_token_by_keyword(self, keyword: str):
        """
        Searches for a virtual token by keyword.

        Args:
            keyword (str): The search keyword.

        Returns:
            dict: Token details or error message.
        """
        from agentipy.tools.evm.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.search_virtual_token_by_keyword(self, keyword)
        except Exception as e:
            raise AgentKitError(f"Failed to search virtual token by keyword: {e}")

    async def get_uniswap_quote(
        self,
        input_token_address: str,
        output_token_address: str,
        amount_in_raw: str,
        input_token_decimals: int = 18,
        output_token_decimals: int = 18,
        slippage: float = 0.5,
        fee_amount: Optional[int] = 3000,
    ):
        """
        Retrieves a quote from Uniswap for swapping between two tokens.

        Args:
            input_token_address (str): The address of the input token.
            output_token_address (str): The address of the output token.
            amount_in_raw (str): The raw amount of input token to swap.
            input_token_decimals (int, optional): The number of decimals for the input token. Defaults to 18.
            output_token_decimals (int, optional): The number of decimals for the output token. Defaults to 18.
            slippage (float, optional): The slippage tolerance percentage. Defaults to 0.5.
            fee_amount (int, optional): The fee amount for the pool. Defaults to 3000 (MEDIUM).

        Returns:
            dict: Quote data or error details.
        """
        if self.network.name != "Base":
            raise AgentKitError("This function is only available for Base network.")

        from agentipy.tools.evm.use_uniswap import UniswapManager

        try:
            return UniswapManager.get_quote(
                self,
                input_token_address,
                output_token_address,
                amount_in_raw,
                input_token_decimals,
                output_token_decimals,
                slippage,
                fee_amount,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to get Uniswap quote: {e}")

    async def trade_on_uniswap(
        self,
        input_token_address: str,
        output_token_address: str,
        amount_in_raw: str,
        input_token_decimals: int = 18,
        output_token_decimals: int = 18,
        slippage: float = 0.5,
        fee_amount: Optional[int] = 3000,
    ):
        """
        Executes a token swap on Uniswap.

        Args:
            input_token_address (str): The address of the input token.
            output_token_address (str): The address of the output token.
            amount_in_raw (str): The raw amount of input token to swap.
            input_token_decimals (int, optional): The number of decimals for the input token. Defaults to 18.
            output_token_decimals (int, optional): The number of decimals for the output token. Defaults to 18.
            slippage (float, optional): The slippage tolerance percentage. Defaults to 0.5.
            fee_amount (int, optional): The fee amount for the pool. Defaults to 3000 (MEDIUM).

        Returns:
            dict: Transaction details or error information.
        """

        if self.network.name != "Base":
            raise AgentKitError("This function is only available for Base network.")

        from agentipy.tools.evm.use_uniswap import UniswapManager

        try:
            return UniswapManager.trade(
                self,
                input_token_address,
                output_token_address,
                amount_in_raw,
                input_token_decimals,
                output_token_decimals,
                slippage,
                fee_amount,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to execute Uniswap trade: {e}")

    async def get_trending_tokens(self):
        """
        Get trending tokens from CoinGecko.

        Returns:
            dict: Trending tokens data.
        """
        from agentipy.tools.use_coingecko import CoingeckoManager

        try:
            return await CoingeckoManager.get_trending_tokens(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch trending tokens: {e}")

    async def get_coin_price_vs(
        self, coin_ids: list[str], vs_currencies: list[str] = ["usd"]
    ):
        """
        Get token price data from CoinGecko.

        Args:
            coin_ids (list[str]): A list of token contract addresses.
            vs_currencies (list[str], optional): A list of currency codes for price comparison. Default is ["usd"].

        Returns:
            dict: Token price data from CoinGecko.
        """
        from agentipy.tools.use_coingecko import CoingeckoManager

        try:
            return await CoingeckoManager.get_coin_price_vs(
                self, coin_ids, vs_currencies
            )
        except Exception as e:
            raise AgentKitError(f"Failed to fetch token price data: {e}")

    async def get_trending_pools(self, duration: str = "24h"):
        """
        Get trending pools from CoinGecko for the Solana network.

        Args:
            duration (str): Duration filter for trending pools. Allowed values: "5m", "1h", "6h", "24h". Default is "24h".

        Returns:
            dict: Trending pools data.
        """
        from agentipy.tools.use_coingecko import CoingeckoManager

        try:
            return await CoingeckoManager.get_trending_pools(self, duration)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch trending pools: {e}")

    async def get_top_gainers(
        self, duration: str = "24h", top_coins: int | str = "all"
    ):
        """
        Get top gainers from CoinGecko.

        Args:
            duration (str): Duration filter for top gainers. Default is "24h".
            top_coins (int or str): The number of top coins to return. Default is "all".

        Returns:
            dict: Top gainers data.
        """
        from agentipy.tools.use_coingecko import CoingeckoManager

        try:
            return await CoingeckoManager.get_top_gainers(self, duration, top_coins)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch top gainers: {e}")

    async def get_token_price_data(self, token_addresses: list[str]):
        """
        Get token price data for a list of token addresses from CoinGecko.

        Args:
            token_addresses (list[str]): A list of token contract addresses.

        Returns:
            dict: Token price data from CoinGecko.
        """
        from agentipy.tools.use_coingecko import CoingeckoManager

        try:
            return await CoingeckoManager.get_token_price_data(self, token_addresses)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch token price data: {e}")

    async def get_token_info(self, token_address: str):
        """
        Get token info for a given token address from CoinGecko.

        Args:
            token_address (str): The token's contract address.

        Returns:
            dict: Token info data.
        """
        from agentipy.tools.use_coingecko import CoingeckoManager

        try:
            return await CoingeckoManager.get_token_info(self, token_address)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch token info: {e}")

    async def get_latest_pools(self):
        """
        Get the latest pools from CoinGecko for the Solana network.

        Returns:
            dict: Latest pools data.
        """
        from agentipy.tools.use_coingecko import CoingeckoManager

        try:
            return await CoingeckoManager.get_latest_pools(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch latest pools: {e}")

    async def stork_fetch_price(self, asset_id: str):
        from agentipy.tools.use_stork import StorkManager

        try:
            return await StorkManager.get_price(self, asset_id)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def ping_elfa_ai_api(self) -> dict:
        """
        Ping the Elfa AI API.

        Returns:
            dict: API response.
        """
        from agentipy.tools.use_elfa_ai import ElfaAiManager

        try:
            return await ElfaAiManager.ping_elfa_ai_api(self)
        except Exception as e:
            raise AgentKitError(f"Failed to ping Elfa AI API: {e}")

    async def get_elfa_ai_api_key_status(self) -> dict:
        """
        Get the Elfa AI API key status.

        Returns:
            dict: API key status.
        """
        from agentipy.tools.use_elfa_ai import ElfaAiManager

        try:
            return await ElfaAiManager.get_elfa_ai_api_key_status(self)
        except Exception as e:
            raise AgentKitError(f"Failed to get Elfa AI API key status: {e}")

    async def get_smart_mentions(self, limit: int = 100, offset: int = 0) -> dict:
        """
        Get smart mentions from Elfa AI.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            limit (int): Number of mentions to retrieve.
            offset (int): Offset for pagination.

        Returns:
            dict: Mentions data.
        """
        from agentipy.tools.use_elfa_ai import ElfaAiManager

        try:
            return await ElfaAiManager.get_smart_mentions(self, limit, offset)
        except Exception as e:
            raise AgentKitError(f"Failed to get smart mentions: {e}")

    async def get_top_mentions_by_ticker(
        self,
        ticker: str,
        time_window: str = "1h",
        page: int = 1,
        page_size: int = 10,
        include_account_details: bool = False,
    ) -> dict:
        """
        Get top mentions by ticker.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            ticker (str): The ticker symbol.
            time_window (str): The time window for mentions.
            page (int): Page number.
            page_size (int): Number of results per page.
            include_account_details (bool): Whether to include account details.

        Returns:
            dict: Mentions data.
        """
        from agentipy.tools.use_elfa_ai import ElfaAiManager

        try:
            return await ElfaAiManager.get_top_mentions_by_ticker(
                self, ticker, time_window, page, page_size, include_account_details
            )
        except Exception as e:
            raise AgentKitError(f"Failed to get top mentions by ticker: {e}")

    async def search_mentions_by_keywords(
        self,
        keywords: str,
        from_timestamp: int,
        to_timestamp: int,
        limit: int = 20,
        cursor: str = None,
    ) -> dict:
        """
        Search mentions by keywords.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            keywords (str): Keywords for search.
            from_timestamp (int): Start timestamp.
            to_timestamp (int): End timestamp.
            limit (int): Number of results to fetch.
            cursor (str): Optional cursor for pagination.

        Returns:
            dict: Search results.
        """
        from agentipy.tools.use_elfa_ai import ElfaAiManager

        try:
            return await ElfaAiManager.search_mentions_by_keywords(
                self, keywords, from_timestamp, to_timestamp, limit, cursor
            )
        except Exception as e:
            raise AgentKitError(f"Failed to search mentions by keywords: {e}")

    async def get_trending_tokens_using_elfa_ai(
        self,
        time_window: str = "24h",
        page: int = 1,
        page_size: int = 50,
        min_mentions: int = 5,
    ) -> dict:
        """
        Get trending tokens using Elfa AI.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            time_window (str): Time window for trending tokens.
            page (int): Page number.
            page_size (int): Number of results per page.
            min_mentions (int): Minimum number of mentions required.

        Returns:
            dict: Trending tokens data.
        """
        from agentipy.tools.use_elfa_ai import ElfaAiManager

        try:
            return await ElfaAiManager.get_trending_tokens_using_elfa_ai(
                self, time_window, page, page_size, min_mentions
            )
        except Exception as e:
            raise AgentKitError(f"Failed to get trending tokens using Elfa AI: {e}")

    async def get_smart_twitter_account_stats(self, username: str) -> dict:
        """
        Get smart Twitter account stats.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            username (str): The Twitter username.

        Returns:
            dict: Account statistics data.
        """
        from agentipy.tools.use_elfa_ai import ElfaAiManager

        try:
            return await ElfaAiManager.get_smart_twitter_account_stats(self, username)
        except Exception as e:
            raise AgentKitError(f"Failed to get smart Twitter account stats: {e}")

    async def get_price_prediction(
        self,
        asset: PriceInferenceToken,
        timeframe: PriceInferenceTimeframe,
        signature_format: SignatureFormat = SignatureFormat.ETHEREUM_SEPOLIA,
    ):
        """
        Fetch a future price prediction for BTC or ETH for a given timeframe (5m or 8h) from the Allora Network.

        :param ticker: The crypto asset symbol (e.g., "BTC" or "ETH").
        :param timeframe: The prediction timeframe ("5m" or "8h").
        :return: A dictionary containing the predicted price and confidence interval.
        """
        from agentipy.tools.use_allora import AlloraManager

        try:
            return await AlloraManager.get_price_prediction(
                self, asset, timeframe, signature_format
            )
        except Exception as e:
            raise AgentKitError(f"Failed to fetch price prediction: {e}")

    async def get_inference_by_topic_id(self, topic_id: int):
        """
        Fetch a price inference for BTC or ETH for a given timeframe (5m or 8h) from the Allora Network.

        :param ticker: The crypto asset symbol (e.g., "BTC" or "ETH").
        :param timeframe: The prediction timeframe ("5m" or "8h").
        :return: A dictionary containing the predicted price and confidence interval.
        """
        from agentipy.tools.use_allora import AlloraManager

        try:
            return await AlloraManager.get_inference_by_topic_id(self, topic_id)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch price inference: {e}")

    async def get_all_topics(self):
        """
        Fetch all topics from the Allora Network.

        :return: A list of topic IDs.
        """
        from agentipy.tools.use_allora import AlloraManager

        try:
            return await AlloraManager.get_all_topics(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch all topics: {e}")

    async def pyth_fetch_price(self, base_token_ticker: str, quote_token_ticker: str):
        from agentipy.tools.use_pyth import PythManager

        try:
            return await PythManager.get_price(
                self, base_token_ticker, quote_token_ticker
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")
