import logging
import os
from typing import Optional

from eth_account import Account
from web3 import Web3

from agentipy.constants import API_VERSION, BASE_PROXY_URL
from agentipy.tools.evm.wallet_opts import Web3EVMClient
from agentipy.utils import AgentKitError
from agentipy.utils.evm.general.networks import Network

logger = logging.getLogger(__name__)

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
        private_key: Optional[str] = None,
        rpc_url: Optional[str] = None,
        rpc_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        generate_wallet: bool = False,
    ):
        self.network = network
        self.rpc_url = rpc_url or os.getenv("EVM_RPC_URL", network.rpc)
        self.rpc_api_key = rpc_api_key or os.getenv("EVM_RPC_API_KEY", "")
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY", "")
        self.chain_id = network.chain_id
        self.token = network.token
        self.explorer = network.explorer
        self.eip1559_support = network.eip1559_support
        self.base_proxy_url = BASE_PROXY_URL
        self.api_version = API_VERSION

        if generate_wallet:
            self.private_key, self.wallet_address = self.generate_wallet()
        else:
            self.private_key = private_key or os.getenv("EVM_PRIVATE_KEY", "")
            if not self.private_key:
                raise AgentKitError("A valid private key must be provided.")
            self.wallet_address = self.web3.eth.account.from_key(self.private_key).address

        self.evm_wallet_client = Web3EVMClient(self.web3,self.private_key)

        if not self.evm_wallet_client:
            raise AgentKitError(f"Failed to connect to {network.name} via {self.rpc_url}")

        logger.info(f"Connected to {network.name} (Chain ID: {self.chain_id}) - RPC: {self.rpc_url}")

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
    
    async def get_sentient_listings(self, page_number: Optional[int] = 1, page_size: Optional[int] = 30):
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
            return  VirtualsManager.get_sentient_listings(self, page_number, page_size)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch Sentient listings: {e}")

    async def buy_sentient(self, token_address: str, amount: str, builder_id: Optional[int] = None):
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
            return  VirtualsManager.buy_sentient(self, token_address, amount, builder_id)
        except Exception as e:
            raise AgentKitError(f"Failed to buy Sentient tokens: {e}")

    async def sell_sentient(self, token_address: str, amount: str, builder_id: Optional[int] = None):
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
            return  VirtualsManager.sell_sentient(self, token_address, amount, builder_id)
        except Exception as e:
            raise AgentKitError(f"Failed to sell Sentient tokens: {e}")

    async def buy_prototype(self, token_address: str, amount: str, builder_id: Optional[int] = None, slippage: Optional[float] = None):
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
            return  VirtualsManager.buy_prototype(self, token_address, amount, builder_id, slippage)
        except Exception as e:
            raise AgentKitError(f"Failed to buy Prototype tokens: {e}")

    async def sell_prototype(self, token_address: str, amount: str, builder_id: Optional[int] = None, slippage: Optional[float] = None):
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
            return  VirtualsManager.sell_prototype(self, token_address, amount, builder_id, slippage)
        except Exception as e:
            raise AgentKitError(f"Failed to sell Prototype tokens: {e}")

    async def check_sentient_allowance(self, amount: str, from_token_address: Optional[str] = None):
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
            return  VirtualsManager.check_sentient_allowance(self, amount, from_token_address)
        except Exception as e:
            raise AgentKitError(f"Failed to check Sentient allowance: {e}")

    async def approve_sentient_allowance(self, amount: str, from_token_address: Optional[str] = None):
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
            return  VirtualsManager.approve_sentient_allowance(self, amount, from_token_address)
        except Exception as e:
            raise AgentKitError(f"Failed to approve Sentient allowance: {e}")

    async def check_prototype_allowance(self, amount: str, from_token_address: Optional[str] = None):
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
            return  VirtualsManager.check_prototype_allowance(self, amount, from_token_address)
        except Exception as e:
            raise AgentKitError(f"Failed to check Prototype allowance: {e}")

    async def approve_prototype_allowance(self, amount: str, from_token_address: Optional[str] = None):
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
            return  VirtualsManager.approve_prototype_allowance(self, amount, from_token_address)
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
            return  VirtualsManager.get_prototype_listing(self, page_number, page_size)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch Prototype listings: {e}")

    async def fetch_klines(self, token_address: str, granularity: int, start: int, end: int, limit: int):
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
            return  VirtualsManager.fetch_klines(self, token_address, granularity, start, end, limit)
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
            return  VirtualsManager.search_virtual_token_by_keyword(self, keyword)
        except Exception as e:
            raise AgentKitError(f"Failed to search virtual token by keyword: {e}")




