import logging
import os
from typing import Any, Dict, List, Optional

import base58
from allora_sdk.v2.api_client import (PriceInferenceTimeframe,
                                      PriceInferenceToken, SignatureFormat)
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from typing_extensions import Union

from agentipy.constants import API_VERSION, BASE_PROXY_URL, DEFAULT_OPTIONS
from agentipy.types import BondingCurveState, PumpfunTokenOptions
from agentipy.utils import AgentKitError
from agentipy.utils.meteora_dlmm.types import ActivationType
from agentipy.wallet.base_wallet_client import BaseWalletClient
from agentipy.wallet.privy_wallet_client import PrivyWalletClient
from agentipy.wallet.solana_wallet_client import SolanaWalletClient

logger = logging.getLogger(__name__)


class SolanaAgentKit:
    """
    Main class for interacting with the Solana blockchain.

    Attributes:
        connection (AsyncClient): Solana RPC connection.
        wallet_client (BaseWalletClient): Wallet client for signing and sending transactions.
        wallet_address (Pubkey): Public key of the wallet.
    """

    def __init__(
        self,
        private_key: Optional[str] = None,
        rpc_url: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        helius_api_key: Optional[str] = None,
        helius_rpc_url: Optional[str] = None,
        backpack_api_key: Optional[str] = None,
        backpack_api_secret: Optional[str] = None,
        quicknode_rpc_url: Optional[str] = None,
        jito_block_engine_url: Optional[str] = None,
        jito_uuid: Optional[str] = None,
        stork_api_key: Optional[str] = None,
        coingecko_api_key: Optional[str] = None,
        coingecko_demo_api_key: Optional[str] = None,
        elfa_ai_api_key: Optional[str] = None,
        flexland_api_key: Optional[str] = None,
        allora_api_key: Optional[str] = None,
        solutiofi_api_key: Optional[str] = None,
        privy_app_id: Optional[str] = None,
        privy_app_secret: Optional[str] = None,
        privy_wallet_id: Optional[str] = None,
        generate_wallet: bool = False,
        use_privy_wallet: bool = False,
    ):
        """
        Initialize the SolanaAgentKit.

        Args:
            private_key (str, optional): Base58-encoded private key for the wallet. Ignored if `generate_wallet` is True.
            rpc_url (str, optional): Solana RPC URL.
            openai_api_key (str, optional): OpenAI API key for additional functionality.
            helius_api_key (str, optional): Helius API key for additional services.
            helius_rpc_url (str, optional): Helius RPC URL.
            quicknode_rpc_url (str, optional): QuickNode RPC URL.
            jito_block_engine_url (str, optional): Jito block engine URL for Solana.
            jito_uuid (str, optional): Jito UUID for authentication.
            privy_app_id (str, optional): Privy App ID for using Privy wallet.
            privy_app_secret (str, optional): Privy App Secret for using Privy wallet.
            generate_wallet (bool): If True, generates a new wallet and returns the details.
            use_privy_wallet (bool): If True, uses Privy wallet instead of local keypair.
        """
        self.rpc_url = rpc_url or os.getenv(
            "SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"
        )
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY", "")
        self.helius_api_key = helius_api_key or os.getenv("HELIUS_API_KEY", "")
        self.helius_rpc_url = helius_rpc_url or os.getenv("HELIUS_RPC_URL", "")
        self.backpack_api_key = backpack_api_key or os.getenv("BACKPACK_API_KEY", "")
        self.backpack_api_secret = backpack_api_secret or os.getenv(
            "BACKPACK_API_SECRET", ""
        )
        self.quicknode_rpc_url = quicknode_rpc_url or os.getenv("QUICKNODE_RPC_URL", "")
        self.jito_block_engine_url = jito_block_engine_url or os.getenv(
            "JITO_BLOCK_ENGINE_URL", ""
        )
        self.jito_uuid = jito_uuid or os.getenv("JITO_UUID", None)
        self.stork_api_key = stork_api_key or os.getenv("STORK_API_KEY", "")
        self.coingecko_api_key = coingecko_api_key or os.getenv(
            "COINGECKO_PRO_API_KEY", ""
        )
        self.coingecko_demo_api_key = coingecko_demo_api_key or os.getenv(
            "COINGECKO_DEMO_API_KEY", ""
        )
        self.elfa_ai_api_key = elfa_ai_api_key or os.getenv("ELFA_AI_API_KEY", "")
        self.flexland_api_key = flexland_api_key or os.getenv("FLEXLAND_API_KEY", "")
        self.allora_api_key = allora_api_key or os.getenv("ALLORA_API_KEY", "")
        self.solutiofi_api_key = solutiofi_api_key or os.getenv("SOLUTIOFI_API_KEY", "")
        self.privy_app_id = privy_app_id or os.getenv("PRIVY_APP_ID", "")
        self.privy_app_secret = privy_app_secret or os.getenv("PRIVY_APP_SECRET", "")
        self.base_proxy_url = BASE_PROXY_URL
        self.api_version = API_VERSION


        self.connection = AsyncClient(self.rpc_url)
        self.connection_client = Client(self.rpc_url)

        if use_privy_wallet:
            if not self.privy_app_id or not self.privy_app_secret:
                raise ValueError(
                    "PRIVY_APP_ID and PRIVY_APP_SECRET must be provided to use Privy wallet."
                )

            # Initialize Privy wallet
            self.wallet_client = PrivyWalletClient(
                self.connection_client,
                self.privy_app_id,
                self.privy_app_secret,
            )

            if generate_wallet:
                wallet_info = self.wallet_client.create_wallet()
                self.wallet_id = wallet_info["id"]
                self.wallet_address = Pubkey.from_string(wallet_info["address"])
                logger.info(f"Created agent for wallet: {privy_wallet_id}")
            else:
                wallet_address = self.wallet_client.use_wallet(privy_wallet_id)

                self.wallet_id = privy_wallet_id
                self.wallet_address = Pubkey.from_string(wallet_address)

        else:
            # Initialize local wallet with keypair
            if generate_wallet:
                self.wallet = Keypair()
                self.wallet_address = self.wallet.pubkey()
                self.private_key = base58.b58encode(self.wallet.secret()).decode(
                    "utf-8"
                )

                logger.info("New Local Wallet Generated:")
                logger.info(f"Public Key: {self.wallet_address}")
                logger.info(f"Private Key: {self.private_key}")
            else:
                self.private_key = private_key or os.getenv("SOLANA_PRIVATE_KEY", "")
                if not self.private_key:
                    raise ValueError(
                        "A valid private key must be provided or a wallet must be generated."
                    )

                self.wallet = Keypair.from_base58_string(self.private_key)
                self.wallet_address = self.wallet.pubkey()

            self.wallet_client = SolanaWalletClient(self.connection_client, self.wallet)

    async def get_wallet_address(self) -> str:
        """
        Get the wallet's address.

        Returns:
            str: The wallet's address in string format.
        """
        return str(self.wallet_address)
    async def request_faucet_funds(self):
        from agentipy.tools.request_faucet_funds import FaucetManager

        try:
            return await FaucetManager.request_faucet_funds(self)
        except Exception as e:
            raise AgentKitError(f"Failed to request faucet funds: {e}")

    async def deploy_token(self, decimals: int = DEFAULT_OPTIONS["TOKEN_DECIMALS"]):
        from agentipy.tools.deploy_token import TokenDeploymentManager

        try:
            return await TokenDeploymentManager.deploy_token(self, decimals)
        except Exception as e:
            raise AgentKitError(f"Failed to deploy token: {e}")

    async def get_balance(self, token_address: Optional[str] = None):
        from agentipy.tools.get_balance import BalanceFetcher

        try:
            return await BalanceFetcher.get_balance(self, token_address)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch balance: {e}")

    async def fetch_price(self, token_id: str):
        from agentipy.tools.fetch_price import TokenPriceFetcher

        try:
            return await TokenPriceFetcher.fetch_price(token_id)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch price: {e}")

    async def transfer(self, to: str, amount: float, mint: Optional[Pubkey] = None):
        from agentipy.tools.transfer import TokenTransferManager

        try:
            return await TokenTransferManager.transfer(self, to, amount, mint)
        except Exception as e:
            raise AgentKitError(f"Failed to execute transfer: {e}")

    async def trade(
        self,
        output_mint: Pubkey,
        input_amount: float,
        input_mint: Optional[Pubkey] = None,
        slippage_bps: int = DEFAULT_OPTIONS["SLIPPAGE_BPS"],
    ):
        from agentipy.tools.trade import TradeManager

        try:
            return await TradeManager.trade(
                self, output_mint, input_amount, input_mint, slippage_bps
            )
        except Exception as e:
            raise AgentKitError(f"Failed to trade: {e}")

    async def lend_assets(self, amount: float):
        from agentipy.tools.use_lulo import LuloManager

        try:
            return await LuloManager.lend_asset(self, amount)
        except Exception as e:
            raise AgentKitError(f"Failed to lend asset: {e}")

    async def lulo_lend(self, mint_address: str, amount: float) -> str:
        """
        Lend tokens for yields using Lulo.

        Args:
            agent (SolanaAgentKit): SolanaAgentKit instance.
            mint_address (str): SPL Mint address.
            amount (float): Amount to lend.

        Returns:
            str: Transaction signature.
        """
        from agentipy.tools.use_lulo import LuloManager

        try:
            return await LuloManager.lulo_lend(self, mint_address, amount)
        except Exception as e:
            raise AgentKitError(f"Failed to lend asset: {e}")

    async def lulo_withdraw(self, mint_address: str, amount: float) -> str:
        """
        Withdraw tokens for yields using Lulo.

        Args:
            agent (SolanaAgentKit): SolanaAgentKit instance.
            mint_address (str): SPL Mint address.
            amount (float): Amount to withdraw.

        Returns:
            str: Transaction signature.
        """
        from agentipy.tools.use_lulo import LuloManager

        try:
            return await LuloManager.lulo_withdraw(self, mint_address, amount)
        except Exception as e:
            raise AgentKitError(f"Failed to withdraw asset: {e}")

    async def get_tps(self):
        from agentipy.tools.get_tps import SolanaPerformanceTracker

        try:
            return await SolanaPerformanceTracker.fetch_current_tps(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch tps: {e}")

    async def get_token_data_by_ticker(self, ticker: str):
        from agentipy.tools.get_token_data import TokenDataManager

        try:
            return TokenDataManager.get_token_data_by_ticker(ticker)
        except Exception as e:
            raise AgentKitError(f"Failed to get token data: {e}")

    async def get_token_data_by_address(self, mint: str):
        from agentipy.tools.get_token_data import TokenDataManager

        try:
            return TokenDataManager.get_token_data_by_address(mint)
        except Exception as e:
            raise AgentKitError(f"Failed to get token data: {e}")

    async def launch_pump_fun_token(
        self,
        token_name: str,
        token_ticker: str,
        description: str,
        image_url: str,
        options: Optional[PumpfunTokenOptions] = None,
    ):
        from agentipy.tools.launch_pumpfun_token import PumpfunTokenManager

        try:
            return await PumpfunTokenManager.launch_pumpfun_token(
                self, token_name, token_ticker, description, image_url, options
            )
        except Exception as e:
            raise AgentKitError(f"Failed to launch token on pumpfun: {e}")

    async def stake(self, amount: int):
        from agentipy.tools.stake_with_jup import StakeManager

        try:
            return await StakeManager.stake_with_jup(self, amount)
        except Exception as e:
            raise AgentKitError(f"Failed to stake: {e}")

    async def create_meteora_dlmm_pool(
        self,
        bin_step: int,
        token_a_mint: Pubkey,
        token_b_mint: Pubkey,
        initial_price: float,
        price_rounding_up: bool,
        fee_bps: int,
        activation_type: ActivationType,
        has_alpha_vault: bool,
        activation_point: Optional[int],
    ):
        from agentipy.tools.create_meteora_dlmm_pool import MeteoraManager

        try:
            return await MeteoraManager.create_meteora_dlmm_pool(
                self,
                bin_step,
                token_a_mint,
                token_b_mint,
                initial_price,
                price_rounding_up,
                fee_bps,
                activation_type,
                has_alpha_vault,
                activation_point,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to create dlmm pool: {e}")

    async def buy_with_raydium(
        self, pair_address: str, sol_in: float = 0.01, slippage: int = 5
    ):
        from agentipy.tools.use_raydium import RaydiumManager

        try:
            return await RaydiumManager.buy_with_raydium(
                self, pair_address, sol_in, slippage
            )
        except Exception as e:
            raise AgentKitError(f"Failed to buy using raydium: {e}")

    async def sell_with_raydium(
        self, pair_address: str, percentage: int = 100, slippage: int = 5
    ):
        from agentipy.tools.use_raydium import RaydiumManager

        try:
            return await RaydiumManager.sell_with_raydium(
                self, pair_address, percentage, slippage
            )
        except Exception as e:
            raise AgentKitError(f"Failed to sell using raydium: {e}")

    async def burn_and_close_accounts(self, token_account: str):
        from agentipy.tools.burn_and_close_account import BurnManager

        try:
            return await BurnManager.burn_and_close_account(self, token_account)
        except Exception as e:
            raise AgentKitError(f"Failed to close account: {e}")

    async def multiple_burn_and_close_accounts(self, token_accounts: list[str]):
        from agentipy.tools.burn_and_close_account import BurnManager

        try:
            return await BurnManager.process_multiple_accounts(self, token_accounts)
        except Exception as e:
            raise AgentKitError(f"Failed to close accounts: {e}")

    async def create_gibwork_task(
        self,
        title: str,
        content: str,
        requirements: str,
        tags: list[str],
        token_mint_address: Pubkey,
        token_amount: int,
    ):
        from agentipy.tools.create_gibwork import GibworkManager

        try:
            return await GibworkManager.create_gibwork_task(
                self,
                title,
                content,
                requirements,
                tags,
                token_mint_address,
                token_amount,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to create task: {e}")

    async def buy_using_moonshot(
        self, mint_str: str, collateral_amount: float = 0.01, slippage_bps: int = 500
    ):
        from agentipy.tools.use_moonshot import MoonshotManager

        try:
            return await MoonshotManager.buy(
                self, mint_str, collateral_amount, slippage_bps
            )
        except Exception as e:
            raise AgentKitError(f"Failed to buy using moonshot: {e}")

    async def sell_using_moonshot(
        self, mint_str: str, token_balance: float = 0.01, slippage_bps: int = 500
    ):
        from agentipy.tools.use_moonshot import MoonshotManager

        try:
            return await MoonshotManager.sell(
                self, mint_str, token_balance, slippage_bps
            )
        except Exception as e:
            raise AgentKitError(f"Failed to sell using moonshot: {e}")

    async def pyth_fetch_price(self, base_token_ticker: str, quote_token_ticker: str):
        from agentipy.tools.use_pyth import PythManager

        try:
            return await PythManager.get_price(
                self, base_token_ticker, quote_token_ticker
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def stork_fetch_price(self, asset_id: str):
        from agentipy.tools.use_stork import StorkManager

        try:
            return await StorkManager.get_price(self, asset_id)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_balances(self, address: str):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_balances(self, address)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_address_name(self, address: str):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_address_name(self, address)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_nft_events(
        self,
        accounts: List[str],
        types: List[str] = None,
        sources: List[str] = None,
        start_slot: int = None,
        end_slot: int = None,
        start_time: int = None,
        end_time: int = None,
        first_verified_creator: List[str] = None,
        verified_collection_address: List[str] = None,
        limit: int = None,
        sort_order: str = None,
        pagination_token: str = None,
    ):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_nft_events(
                self,
                accounts,
                types,
                sources,
                start_slot,
                end_slot,
                start_time,
                end_time,
                first_verified_creator,
                verified_collection_address,
                limit,
                sort_order,
                pagination_token,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_mintlists(
        self,
        first_verified_creators: List[str],
        verified_collection_addresses: List[str] = None,
        limit: int = None,
        pagination_token: str = None,
    ):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_mintlists(
                self,
                first_verified_creators,
                verified_collection_addresses,
                limit,
                pagination_token,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_nft_fingerprint(self, mints: List[str]):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_nft_fingerprint(self, mints)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_active_listings(
        self,
        first_verified_creators: List[str],
        verified_collection_addresses: List[str] = None,
        marketplaces: List[str] = None,
        limit: int = None,
        pagination_token: str = None,
    ):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_active_listings(
                self,
                first_verified_creators,
                verified_collection_addresses,
                marketplaces,
                limit,
                pagination_token,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_nft_metadata(self, mint_accounts: List[str]):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_nft_metadata(self, mint_accounts)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_raw_transactions(
        self,
        accounts: List[str],
        start_slot: int = None,
        end_slot: int = None,
        start_time: int = None,
        end_time: int = None,
        limit: int = None,
        sort_order: str = None,
        pagination_token: str = None,
    ):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_raw_transactions(
                self,
                accounts,
                start_slot,
                end_slot,
                start_time,
                end_time,
                limit,
                sort_order,
                pagination_token,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_parsed_transactions(
        self, transactions: List[str], commitment: str = None
    ):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_parsed_transactions(self, transactions, commitment)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_parsed_transaction_history(
        self,
        address: str,
        before: str = "",
        until: str = "",
        commitment: str = "",
        source: str = "",
        type: str = "",
    ):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_parsed_transaction_history(
                self, address, before, until, commitment, source, type
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def create_webhook(
        self,
        webhook_url: str,
        transaction_types: list,
        account_addresses: list,
        webhook_type: str,
        txn_status: str = "all",
        auth_header: str = None,
    ):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.create_webhook(
                self,
                webhook_url,
                transaction_types,
                account_addresses,
                webhook_type,
                txn_status,
                auth_header,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_all_webhooks(self):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_all_webhooks(self)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_webhook(self, webhook_id: str):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.get_webhook(self, webhook_id)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def edit_webhook(
        self,
        webhook_id: str,
        webhook_url: str,
        transaction_types: list,
        account_addresses: list,
        webhook_type: str,
        txn_status: str = "all",
        auth_header: str = None,
    ):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.edit_webhook(
                self,
                webhook_id,
                webhook_url,
                transaction_types,
                account_addresses,
                webhook_type,
                txn_status,
                auth_header,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def delete_webhook(self, webhook_id: str):
        from agentipy.tools.use_helius import HeliusManager

        try:
            return HeliusManager.delete_webhook(self, webhook_id)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def fetch_token_report_summary(mint: str):
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_token_report_summary(mint)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def fetch_token_detailed_report(mint: str):
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_token_detailed_report(mint)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def fetch_all_domains(page: int = 1, limit: int = 50, verified: bool = False):
        """
        Fetches all registered domains with optional pagination and filtering.

        Args:
            page (int): The page number for pagination (default is 1).
            limit (int): The number of records per page (default is 50).
            verified (bool, optional): Filter for verified domains.

        Returns:
            list: A list of all registered domains.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_all_domains(page, limit, verified)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch all domains: {e}")

    async def fetch_domains_csv(verified: bool = False):
        """
        Fetches all registered domains in CSV format.

        Args:
            verified (bool, optional): Filter for verified domains.

        Returns:
            str: A CSV string with all registered domains.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_domains_csv(verified)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch domains CSV: {e}")

    async def lookup_domain(domain: str):
        """
        Looks up a domain by name.

        Args:
            domain (str): The domain name to look up.

        Returns:
            dict: The domain details.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.lookup_domain(domain)
        except Exception as e:
            raise AgentKitError(f"Failed to lookup domain: {e}")

    async def fetch_domain_records(domain: str):
        """
        Fetches all records for a domain.

        Args:
            domain (str): The domain name.

        Returns:
            list: A list of all records for the domain.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_domain_records(domain)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch domain records: {e}")

    async def fetch_leaderboard():
        """
        Fetches the leaderboard with optional pagination.

        Args:
            page (int): The page number for pagination (default is 1).
            limit (int): The number of records per page (default is 50).

        Returns:
            list: A list of leaderboard entries.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_leaderboard()
        except Exception as e:
            raise AgentKitError(f"Failed to fetch leaderboard: {e}")

    async def fetch_new_tokens():
        """
        Fetches new tokens with optional pagination.

        Args:
            page (int): The page number for pagination (default is 1).
            limit (int): The number of records per page (default is 50).

        Returns:
            list: A list of new tokens.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_new_tokens()
        except Exception as e:
            raise AgentKitError(f"Failed to fetch new tokens: {e}")

    async def fetch_most_viewed_tokens():
        """
        Fetches the most viewed tokens with optional pagination.

        Args:
            page (int): The page number for pagination (default is 1).
            limit (int): The number of records per page (default is 50).

        Returns:
            list: A list of most viewed tokens.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_most_viewed_tokens()
        except Exception as e:
            raise AgentKitError(f"Failed to fetch most viewed tokens: {e}")

    async def fetch_trending_tokens():
        """
        Fetches trending tokens with optional pagination.

        Args:
            page (int): The page number for pagination (default is 1).
            limit (int): The number of records per page (default is 50).

        Returns:
            list: A list of trending tokens.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_trending_tokens()
        except Exception as e:
            raise AgentKitError(f"Failed to fetch trending tokens: {e}")

    async def fetch_recently_verified_tokens():
        """
        Fetches recently verified tokens with optional pagination.

        Args:
            page (int): The page number for pagination (default is 1).
            limit (int): The number of records per page (default is 50).

        Returns:
            list: A list of recently verified tokens.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_recently_verified_tokens()
        except Exception as e:
            raise AgentKitError(f"Failed to fetch recently verified tokens: {e}")

    async def fetch_token_lp_lockers(token_id: str):
        """
        Fetches token LP lockers with optional pagination.

        Args:
            page (int): The page number for pagination (default is 1).
            limit (int): The number of records per page (default is 50).

        Returns:
            list: A list of token LP lockers.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_token_lp_lockers(token_id)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch token LP lockers: {e}")

    async def fetch_token_flux_lp_lockers(token_id: str):
        """
        Fetches token flux LP lockers with optional pagination.

        Args:
            page (int): The page number for pagination (default is 1).
            limit (int): The number of records per page (default is 50).

        Returns:
            list: A list of token flux LP lockers.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_token_flux_lp_lockers(token_id)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch token flux LP lockers: {e}")

    async def fetch_token_votes(mint: str):
        """
        Fetches token votes with optional pagination.

        Args:
            page (int): The page number for pagination (default is 1).
            limit (int): The number of records per page (default is 50).

        Returns:
            list: A list of token votes.

        Raises:
            Exception: If the API call fails.
        """
        from agentipy.tools.rugcheck import RugCheckManager

        try:
            return await RugCheckManager.fetch_token_votes(mint)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch token votes: {e}")

    async def get_pump_curve_state(
        conn: AsyncClient,
        curve_address: Pubkey,
    ):
        from agentipy.tools.use_pumpfun import PumpfunManager

        try:
            return PumpfunManager.get_pump_curve_state(conn, curve_address)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def calculate_pump_curve_price(curve_state: BondingCurveState):
        from agentipy.tools.use_pumpfun import PumpfunManager

        try:
            return PumpfunManager.calculate_pump_curve_price(curve_state)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def buy_token(
        self,
        mint: Pubkey,
        bonding_curve: Pubkey,
        associated_bonding_curve: Pubkey,
        amount: float,
        slippage: float,
        max_retries: int,
    ):
        from agentipy.tools.use_pumpfun import PumpfunManager

        try:
            return PumpfunManager.buy_token(
                self,
                mint,
                bonding_curve,
                associated_bonding_curve,
                amount,
                slippage,
                max_retries,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def sell_token(
        self,
        mint: Pubkey,
        bonding_curve: Pubkey,
        associated_bonding_curve: Pubkey,
        amount: float,
        slippage: float,
        max_retries: int,
    ):
        from agentipy.tools.use_pumpfun import PumpfunManager

        try:
            return PumpfunManager.sell_token(
                self,
                mint,
                bonding_curve,
                associated_bonding_curve,
                slippage,
                max_retries,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def resolve_name_to_address(self, domain: str):
        from agentipy.tools.use_sns import NameServiceManager

        try:
            return NameServiceManager.resolve_name_to_address(self, domain)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_favourite_domain(self, owner: str):
        from agentipy.tools.use_sns import NameServiceManager

        try:
            return NameServiceManager.get_favourite_domain(self, owner)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_all_domains_for_owner(self, owner: str):
        from agentipy.tools.use_sns import NameServiceManager

        try:
            return NameServiceManager.get_all_domains_for_owner(self, owner)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_registration_transaction(
        self,
        domain: str,
        buyer: str,
        buyer_token_account: str,
        space: int,
        mint: Optional[str] = None,
        referrer_key: Optional[str] = None,
    ):
        from agentipy.tools.use_sns import NameServiceManager

        try:
            return NameServiceManager.get_registration_transaction(
                self, domain, buyer, buyer_token_account, space, mint, referrer_key
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def deploy_collection(
        self, name: str, uri: str, royalty_basis_points: int, creator_address: str
    ):
        from agentipy.tools.use_metaplex import DeployCollectionManager

        try:
            return DeployCollectionManager.deploy_collection(
                self, name, uri, royalty_basis_points, creator_address
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_metaplex_asset(self, assetId: str):
        from agentipy.tools.use_metaplex import DeployCollectionManager

        try:
            return DeployCollectionManager.get_metaplex_asset(self, assetId)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_metaplex_assets_by_creator(
        self,
        creator: str,
        onlyVerified: bool = False,
        sortBy: Union[str, None] = None,
        sortDirection: Union[str, None] = None,
        limit: Union[int, None] = None,
        page: Union[int, None] = None,
        before: Union[str, None] = None,
        after: Union[str, None] = None,
    ):
        from agentipy.tools.use_metaplex import DeployCollectionManager

        try:
            return DeployCollectionManager.get_metaplex_assets_by_creator(
                self,
                creator,
                onlyVerified,
                sortBy,
                sortDirection,
                limit,
                page,
                before,
                after,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_metaplex_assets_by_authority(
        self,
        authority: str,
        sortBy: Union[str, None] = None,
        sortDirection: Union[str, None] = None,
        limit: Union[int, None] = None,
        page: Union[int, None] = None,
        before: Union[str, None] = None,
        after: Union[str, None] = None,
    ):
        from agentipy.tools.use_metaplex import DeployCollectionManager

        try:
            return DeployCollectionManager.get_metaplex_assets_by_authority(
                self, authority, sortBy, sortDirection, limit, page, before, after
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def mint_metaplex_core_nft(
        self,
        collectionMint: str,
        name: str,
        uri: str,
        sellerFeeBasisPoints: Union[int, None] = None,
        address: Union[str, None] = None,
        share: Union[str, None] = None,
        recipient: Union[str, None] = None,
    ):
        from agentipy.tools.use_metaplex import DeployCollectionManager

        try:
            return DeployCollectionManager.mint_metaplex_core_nft(
                self,
                collectionMint,
                name,
                uri,
                sellerFeeBasisPoints,
                address,
                share,
                recipient,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def create_debridge_transaction(
        self,
        src_chain_id: str,
        src_chain_token_in: str,
        src_chain_token_in_amount: str,
        dst_chain_id: str,
        dst_chain_token_out: str,
        dst_chain_token_out_recipient: str,
        src_chain_order_authority_address: str,
        dst_chain_order_authority_address: str,
        affiliate_fee_percent: str = "0",
        affiliate_fee_recipient: str = "",
        prepend_operating_expenses: bool = True,
        dst_chain_token_out_amount: str = "auto",
    ):
        from agentipy.tools.use_debridge import DeBridgeManager

        try:
            return DeBridgeManager.create_debridge_transaction(
                self,
                src_chain_id,
                src_chain_token_in,
                src_chain_token_in_amount,
                dst_chain_id,
                dst_chain_token_out,
                dst_chain_token_out_recipient,
                src_chain_order_authority_address,
                dst_chain_order_authority_address,
                affiliate_fee_percent,
                affiliate_fee_recipient,
                prepend_operating_expenses,
                dst_chain_token_out_amount,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def execute_debridge_transaction(self, transaction_data: dict):
        from agentipy.tools.use_debridge import DeBridgeManager

        try:
            return await DeBridgeManager.execute_debridge_transaction(
                self, transaction_data
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def check_transaction_status(self, tx_hash: str):
        from agentipy.tools.use_debridge import DeBridgeManager

        try:
            return await DeBridgeManager.check_transaction_status(self, tx_hash)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def cybers_create_coin(
        self,
        name: str,
        symbol: str,
        image_path: str,
        tweet_author_id: str,
        tweet_author_username: str,
    ):
        from agentipy.tools.use_cybers import CybersManager

        try:
            return CybersManager.create_coin(
                self, name, symbol, image_path, tweet_author_id, tweet_author_username
            )
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_tip_accounts(self):
        from agentipy.tools.use_jito import JitoManager

        try:
            return JitoManager.get_tip_accounts(self)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_random_tip_account():
        from agentipy.tools.use_jito import JitoManager

        try:
            return JitoManager.get_random_tip_account()
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_bundle_statuses(self, bundle_uuids):
        from agentipy.tools.use_jito import JitoManager

        try:
            return JitoManager.get_bundle_statuses(self, bundle_uuids)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def send_bundle(self, params=None):
        from agentipy.tools.use_jito import JitoManager

        try:
            return JitoManager.send_bundle(self, params)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_inflight_bundle_statuses(self, bundle_uuids):
        from agentipy.tools.use_jito import JitoManager

        try:
            return JitoManager.get_inflight_bundle_statuses(self, bundle_uuids)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def send_txn(self, params=None, bundleOnly=False):
        from agentipy.tools.use_jito import JitoManager

        try:
            return JitoManager.send_txn(self, params, bundleOnly)
        except Exception as e:
            raise AgentKitError(f"Failed to {e}")

    async def get_account_balances(self):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_account_balances(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch account balances: {e}")

    async def request_withdrawal(
        self, address: str, blockchain: str, quantity: str, symbol: str, **kwargs
    ):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.request_withdrawal(
                self, address, blockchain, quantity, symbol, **kwargs
            )
        except Exception as e:
            raise AgentKitError(f"Failed to request withdrawal: {e}")

    async def get_account_settings(self):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_account_settings(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch account settings: {e}")

    async def update_account_settings(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.update_account_settings(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to update account settings: {e}")

    async def get_borrow_lend_positions(self):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_borrow_lend_positions(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch borrow/lend positions: {e}")

    async def execute_borrow_lend(self, quantity: str, side: str, symbol: str):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.execute_borrow_lend(
                self, quantity, side, symbol
            )
        except Exception as e:
            raise AgentKitError(f"Failed to execute borrow/lend operation: {e}")

    async def get_collateral_info(self, sub_account_id: int = None):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_collateral_info(self, sub_account_id)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch collateral information: {e}")

    async def get_account_deposits(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_account_deposits(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch account deposits: {e}")

    async def get_open_positions(self):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_open_positions(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch open positions: {e}")

    async def get_borrow_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_borrow_history(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch borrow history: {e}")

    async def get_interest_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_interest_history(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch interest history: {e}")

    async def get_fill_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_fill_history(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch fill history: {e}")

    async def get_borrow_position_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_borrow_position_history(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch borrow position history: {e}")

    async def get_funding_payments(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_funding_payments(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch funding payments: {e}")

    async def get_order_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_order_history(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch order history: {e}")

    async def get_pnl_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_pnl_history(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch PNL history: {e}")

    async def get_settlement_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_settlement_history(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch settlement history: {e}")

    async def get_users_open_orders(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_users_open_orders(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch user's open orders: {e}")

    async def execute_order(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.execute_order(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to execute order: {e}")

    async def cancel_open_order(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.cancel_open_order(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to cancel open order: {e}")

    async def get_open_orders(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_open_orders(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch open orders: {e}")

    async def cancel_open_orders(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.cancel_open_orders(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to cancel open orders: {e}")

    async def get_supported_assets(self):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_supported_assets(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch supported assets: {e}")

    async def get_ticker_information(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_ticker_information(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch ticker information: {e}")

    async def get_markets(self):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_markets(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch markets: {e}")

    async def get_market(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_market(self, **kwargs)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch market: {e}")

    async def get_tickers(self):
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_tickers(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch tickers: {e}")

    async def get_depth(self, symbol: str):
        """
        Retrieves the order book depth for a given market symbol.

        Args:
            symbol (str): Market symbol.

        Returns:
            dict: Order book depth.
        """
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_depth(self, symbol)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch order book depth: {e}")

    async def get_klines(
        self, symbol: str, interval: str, start_time: int, end_time: int = None
    ):
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
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_klines(
                self, symbol, interval, start_time, end_time
            )
        except Exception as e:
            raise AgentKitError(f"Failed to fetch K-Lines: {e}")

    async def get_mark_price(self, symbol: str):
        """
        Retrieves mark price, index price, and funding rate for the given market symbol.

        Args:
            symbol (str): Market symbol.

        Returns:
            dict: Mark price data.
        """
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_mark_price(self, symbol)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch mark price: {e}")

    async def get_open_interest(self, symbol: str):
        """
        Retrieves the current open interest for the given market.

        Args:
            symbol (str): Market symbol.

        Returns:
            dict: Open interest data.
        """
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_open_interest(self, symbol)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch open interest: {e}")

    async def get_funding_interval_rates(
        self, symbol: str, limit: int = 100, offset: int = 0
    ):
        """
        Funding interval rate history for futures.

        Args:
            symbol (str): Market symbol.
            limit (int, optional): Maximum results to return. Defaults to 100.
            offset (int, optional): Records to skip. Defaults to 0.

        Returns:
            dict: Funding interval rate data.
        """
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_funding_interval_rates(
                self, symbol, limit, offset
            )
        except Exception as e:
            raise AgentKitError(f"Failed to fetch funding interval rates: {e}")

    async def get_status(self):
        """
        Get the system status and the status message, if any.

        Returns:
            dict: System status.
        """
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_status(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch system status: {e}")

    async def send_ping(self):
        """
        Responds with pong.

        Returns:
            str: "pong"
        """
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.send_ping(self)
        except Exception as e:
            raise AgentKitError(f"Failed to send ping: {e}")

    async def get_system_time(self):
        """
        Retrieves the current system time.

        Returns:
            str: Current system time.
        """
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_system_time(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch system time: {e}")

    async def get_recent_trades(self, symbol: str, limit: int = 100):
        """
        Retrieve the most recent trades for a symbol.

        Args:
            symbol (str): Market symbol.
            limit (int, optional): Maximum results to return. Defaults to 100.

        Returns:
            dict: Recent trade data.
        """
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_recent_trades(self, symbol, limit)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch recent trades: {e}")

    async def get_historical_trades(
        self, symbol: str, limit: int = 100, offset: int = 0
    ):
        """
        Retrieves all historical trades for the given symbol.

        Args:
            symbol (str): Market symbol.
            limit (int, optional): Maximum results to return. Defaults to 100.
            offset (int, optional): Records to skip. Defaults to 0.

        Returns:
            dict: Historical trade data.
        """
        from agentipy.tools.use_backpack import BackpackManager

        try:
            return await BackpackManager.get_historical_trades(
                self, symbol, limit, offset
            )
        except Exception as e:
            raise AgentKitError(f"Failed to fetch historical trades: {e}")

    async def close_perp_trade_short(
        self, price: float, trade_mint: str
    ) -> Optional[Dict[str, Any]]:
        """
        Closes a perpetual short trade.

        Args:
            price (float): Execution price for closing the trade.
            trade_mint (str): Token mint address for the trade.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_adrena import AdrenaTradeManager

            return await AdrenaTradeManager.close_perp_trade_short(
                self, price, trade_mint
            )
        except Exception as e:
            raise AgentKitError(f"Failed to close perp short trade: {e}")

    async def close_perp_trade_long(
        self, price: float, trade_mint: str
    ) -> Optional[Dict[str, Any]]:
        """
        Closes a perpetual long trade.

        Args:
            price (float): Execution price for closing the trade.
            trade_mint (str): Token mint address for the trade.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_adrena import AdrenaTradeManager

            return await AdrenaTradeManager.close_perp_trade_long(
                self, price, trade_mint
            )
        except Exception as e:
            raise AgentKitError(f"Failed to close perp long trade: {e}")

    async def open_perp_trade_long(
        self,
        price: float,
        collateral_amount: float,
        collateral_mint: Optional[str] = None,
        leverage: Optional[float] = None,
        trade_mint: Optional[str] = None,
        slippage: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Opens a perpetual long trade.

        Args:
            price (float): Entry price for the trade.
            collateral_amount (float): Amount of collateral.
            collateral_mint (str, optional): Mint address of the collateral.
            leverage (float, optional): Leverage factor.
            trade_mint (str, optional): Token mint address.
            slippage (float, optional): Slippage tolerance.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_adrena import AdrenaTradeManager

            return await AdrenaTradeManager.open_perp_trade_long(
                self,
                price,
                collateral_amount,
                collateral_mint,
                leverage,
                trade_mint,
                slippage,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to open perp long trade: {e}")

    async def open_perp_trade_short(
        self,
        price: float,
        collateral_amount: float,
        collateral_mint: Optional[str] = None,
        leverage: Optional[float] = None,
        trade_mint: Optional[str] = None,
        slippage: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Opens a perpetual short trade.

        Args:
            price (float): Entry price for the trade.
            collateral_amount (float): Amount of collateral.
            collateral_mint (str, optional): Mint address of the collateral.
            leverage (float, optional): Leverage factor.
            trade_mint (str, optional): Token mint address.
            slippage (float, optional): Slippage tolerance.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_adrena import AdrenaTradeManager

            return await AdrenaTradeManager.open_perp_trade_short(
                self,
                price,
                collateral_amount,
                collateral_mint,
                leverage,
                trade_mint,
                slippage,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to open perp short trade: {e}")

    async def create_3land_collection(
        self,
        collection_symbol: str,
        collection_name: str,
        collection_description: str,
        main_image_url: Optional[str] = None,
        cover_image_url: Optional[str] = None,
        is_devnet: Optional[bool] = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a 3land NFT collection.

        Args:
            collection_symbol (str): Symbol of the collection.
            collection_name (str): Name of the collection.
            collection_description (str): Description of the collection.
            main_image_url (str, optional): URL of the main image.
            cover_image_url (str, optional): URL of the cover image.
            is_devnet (bool, optional): Whether to use devnet.

        Returns:
            dict: Transaction details.
        """
        from agentipy.tools.use_3land import ThreeLandManager

        try:
            return await ThreeLandManager.create_3land_collection(
                self,
                collection_symbol,
                collection_name,
                collection_description,
                main_image_url,
                cover_image_url,
                is_devnet,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to create 3land collection: {e}")

    async def create_3land_nft(
        self,
        item_name: str,
        seller_fee: float,
        item_amount: int,
        item_symbol: str,
        item_description: str,
        traits: Any,
        price: Optional[float] = None,
        main_image_url: Optional[str] = None,
        cover_image_url: Optional[str] = None,
        spl_hash: Optional[str] = None,
        pool_name: Optional[str] = None,
        is_devnet: Optional[bool] = False,
        with_pool: Optional[bool] = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a 3land NFT.

        Args:
            item_name (str): Name of the NFT.
            seller_fee (float): Seller fee percentage.
            item_amount (int): Number of NFTs to mint.
            item_symbol (str): Symbol of the NFT.
            item_description (str): Description of the NFT.
            traits (Any): NFT traits.
            price (float, optional): Price of the NFT.
            main_image_url (str, optional): URL of the main image.
            cover_image_url (str, optional): URL of the cover image.
            spl_hash (str, optional): SPL hash identifier.
            pool_name (str, optional): Pool name.
            is_devnet (bool, optional): Whether to use devnet.
            with_pool (bool, optional): Whether to include a pool.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_3land import ThreeLandManager

            return await ThreeLandManager.create_3land_nft(
                self,
                item_name,
                seller_fee,
                item_amount,
                item_symbol,
                item_description,
                traits,
                price,
                main_image_url,
                cover_image_url,
                spl_hash,
                pool_name,
                is_devnet,
                with_pool,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to create 3land NFT: {e}")

    async def create_drift_user_account(
        self, deposit_amount: float, deposit_symbol: str
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a Drift user account with an initial deposit.

        Args:
            deposit_amount (float): Amount to deposit.
            deposit_symbol (str): Symbol of the asset to deposit.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.create_drift_user_account(
                self, deposit_amount, deposit_symbol
            )
        except Exception as e:
            raise AgentKitError(f"Failed to create Drift user account: {e}")

    async def deposit_to_drift_user_account(
        self, amount: float, symbol: str, is_repayment: Optional[bool] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Deposits funds into a Drift user account.

        Args:
            amount (float): Amount to deposit.
            symbol (str): Symbol of the asset.
            is_repayment (bool, optional): Whether the deposit is a loan repayment.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.deposit_to_drift_user_account(
                self, amount, symbol, is_repayment
            )
        except Exception as e:
            raise AgentKitError(f"Failed to deposit to Drift user account: {e}")

    async def withdraw_from_drift_user_account(
        self, amount: float, symbol: str, is_borrow: Optional[bool] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Withdraws funds from a Drift user account.

        Args:
            amount (float): Amount to withdraw.
            symbol (str): Symbol of the asset.
            is_borrow (bool, optional): Whether the withdrawal is a borrow request.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.withdraw_from_drift_user_account(
                self, amount, symbol, is_borrow
            )
        except Exception as e:
            raise AgentKitError(f"Failed to withdraw from Drift user account: {e}")

    async def trade_using_drift_perp_account(
        self,
        amount: float,
        symbol: str,
        action: str,
        trade_type: str,
        price: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Executes a trade using a Drift perpetual account.

        Args:
            amount (float): Trade amount.
            symbol (str): Market symbol.
            action (str): "long" or "short".
            trade_type (str): "market" or "limit".
            price (float, optional): Trade execution price.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.trade_using_drift_perp_account(
                self, amount, symbol, action, trade_type, price
            )
        except Exception as e:
            raise AgentKitError(f"Failed to trade using Drift perp account: {e}")

    async def check_if_drift_account_exists(self) -> Optional[Dict[str, Any]]:
        """
        Checks if a Drift user account exists.

        Returns:
            dict: Boolean indicating account existence.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.check_if_drift_account_exists(self)
        except Exception as e:
            raise AgentKitError(f"Failed to check Drift account existence: {e}")

    async def drift_user_account_info(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves Drift user account information.

        Returns:
            dict: Account details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.drift_user_account_info(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch Drift user account info: {e}")

    async def get_available_drift_markets(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves available markets on Drift.

        Returns:
            dict: List of available Drift markets.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.get_available_drift_markets(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch available Drift markets: {e}")

    async def stake_to_drift_insurance_fund(
        self, amount: float, symbol: str
    ) -> Optional[Dict[str, Any]]:
        """
        Stakes funds into the Drift insurance fund.

        Args:
            amount (float): Amount to stake.
            symbol (str): Token symbol.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.stake_to_drift_insurance_fund(
                self, amount, symbol
            )
        except Exception as e:
            raise AgentKitError(f"Failed to stake to Drift insurance fund: {e}")

    async def request_unstake_from_drift_insurance_fund(
        self, amount: float, symbol: str
    ) -> Optional[Dict[str, Any]]:
        """
        Requests unstaking from the Drift insurance fund.

        Args:
            amount (float): Amount to unstake.
            symbol (str): Token symbol.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.request_unstake_from_drift_insurance_fund(
                self, amount, symbol
            )
        except Exception as e:
            raise AgentKitError(
                f"Failed to request unstake from Drift insurance fund: {e}"
            )

    async def unstake_from_drift_insurance_fund(
        self, symbol: str
    ) -> Optional[Dict[str, Any]]:
        """
        Completes an unstaking request from the Drift insurance fund.

        Args:
            symbol (str): Token symbol.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.unstake_from_drift_insurance_fund(self, symbol)
        except Exception as e:
            raise AgentKitError(f"Failed to unstake from Drift insurance fund: {e}")

    async def drift_swap_spot_token(
        self,
        from_symbol: str,
        to_symbol: str,
        slippage: Optional[float] = None,
        to_amount: Optional[float] = None,
        from_amount: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Swaps spot tokens on Drift.

        Args:
            from_symbol (str): Token to swap from.
            to_symbol (str): Token to swap to.
            slippage (float, optional): Allowed slippage.
            to_amount (float, optional): Desired amount of the output token.
            from_amount (float, optional): Amount of the input token.

        Returns:
            dict: Swap transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.drift_swap_spot_token(
                self, from_symbol, to_symbol, slippage, to_amount, from_amount
            )
        except Exception as e:
            raise AgentKitError(f"Failed to swap spot token on Drift: {e}")

    async def get_drift_perp_market_funding_rate(
        self, symbol: str, period: str = "year"
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves the funding rate for a Drift perpetual market.

        Args:
            symbol (str): Market symbol (must end in '-PERP').
            period (str, optional): Funding rate period, either "year" or "hour". Defaults to "year".

        Returns:
            dict: Funding rate information.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.get_drift_perp_market_funding_rate(
                self, symbol, period
            )
        except Exception as e:
            raise AgentKitError(f"Failed to get Drift perp market funding rate: {e}")

    async def get_drift_entry_quote_of_perp_trade(
        self, amount: float, symbol: str, action: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves the entry quote for a perpetual trade on Drift.

        Args:
            amount (float): Trade amount.
            symbol (str): Market symbol (must end in '-PERP').
            action (str): "long" or "short".

        Returns:
            dict: Entry quote details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.get_drift_entry_quote_of_perp_trade(
                self, amount, symbol, action
            )
        except Exception as e:
            raise AgentKitError(f"Failed to get Drift entry quote of perp trade: {e}")

    async def get_drift_lend_borrow_apy(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the lending and borrowing APY for a given symbol on Drift.

        Args:
            symbol (str): Token symbol.

        Returns:
            dict: Lending and borrowing APY details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.get_drift_lend_borrow_apy(self, symbol)
        except Exception as e:
            raise AgentKitError(f"Failed to get Drift lend/borrow APY: {e}")

    async def create_drift_vault(
        self,
        name: str,
        market_name: str,
        redeem_period: int,
        max_tokens: int,
        min_deposit_amount: float,
        management_fee: float,
        profit_share: float,
        hurdle_rate: Optional[float] = None,
        permissioned: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a Drift vault.

        Args:
            name (str): Vault name.
            market_name (str): Market name format '<name>-<name>'.
            redeem_period (int): Redeem period in blocks.
            max_tokens (int): Maximum number of tokens.
            min_deposit_amount (float): Minimum deposit amount.
            management_fee (float): Management fee percentage.
            profit_share (float): Profit share percentage.
            hurdle_rate (float, optional): Hurdle rate.
            permissioned (bool, optional): Whether the vault is permissioned.

        Returns:
            dict: Vault creation details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.create_drift_vault(
                self,
                name,
                market_name,
                redeem_period,
                max_tokens,
                min_deposit_amount,
                management_fee,
                profit_share,
                hurdle_rate,
                permissioned,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to create Drift vault: {e}")

    async def update_drift_vault_delegate(
        self, vault: str, delegate_address: str
    ) -> Optional[Dict[str, Any]]:
        """
        Updates the delegate address for a Drift vault.

        Args:
            vault (str): Vault address.
            delegate_address (str): New delegate address.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.update_drift_vault_delegate(
                self, vault, delegate_address
            )
        except Exception as e:
            raise AgentKitError(f"Failed to update Drift vault delegate: {e}")

    async def update_drift_vault(
        self,
        vault_address: str,
        name: str,
        market_name: str,
        redeem_period: int,
        max_tokens: int,
        min_deposit_amount: float,
        management_fee: float,
        profit_share: float,
        hurdle_rate: Optional[float] = None,
        permissioned: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Updates an existing Drift vault.

        Args:
            vault_address (str): Address of the vault.
            name (str): Vault name.
            market_name (str): Market name format '<name>-<name>'.
            redeem_period (int): Redeem period in blocks.
            max_tokens (int): Maximum number of tokens.
            min_deposit_amount (float): Minimum deposit amount.
            management_fee (float): Management fee percentage.
            profit_share (float): Profit share percentage.
            hurdle_rate (float, optional): Hurdle rate.
            permissioned (bool, optional): Whether the vault is permissioned.

        Returns:
            dict: Vault update details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.update_drift_vault(
                self,
                vault_address,
                name,
                market_name,
                redeem_period,
                max_tokens,
                min_deposit_amount,
                management_fee,
                profit_share,
                hurdle_rate,
                permissioned,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to update Drift vault: {e}")

    async def get_drift_vault_info(self, vault_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves information about a specific Drift vault.

        Args:
            vault_name (str): Name of the vault.

        Returns:
            dict: Vault details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.get_drift_vault_info(self, vault_name)
        except Exception as e:
            raise AgentKitError(f"Failed to get Drift vault info: {e}")

    async def deposit_into_drift_vault(
        self, amount: float, vault: str
    ) -> Optional[Dict[str, Any]]:
        """
        Deposits funds into a Drift vault.

        Args:
            amount (float): Amount to deposit.
            vault (str): Vault address.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.deposit_into_drift_vault(self, amount, vault)
        except Exception as e:
            raise AgentKitError(f"Failed to deposit into Drift vault: {e}")

    async def request_withdrawal_from_drift_vault(
        self, amount: float, vault: str
    ) -> Optional[Dict[str, Any]]:
        """
        Requests a withdrawal from a Drift vault.

        Args:
            amount (float): Amount to withdraw.
            vault (str): Vault address.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.request_withdrawal_from_drift_vault(
                self, amount, vault
            )
        except Exception as e:
            raise AgentKitError(f"Failed to request withdrawal from Drift vault: {e}")

    async def withdraw_from_drift_vault(self, vault: str) -> Optional[Dict[str, Any]]:
        """
        Withdraws funds from a Drift vault after a withdrawal request.

        Args:
            vault (str): Vault address.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.withdraw_from_drift_vault(self, vault)
        except Exception as e:
            raise AgentKitError(f"Failed to withdraw from Drift vault: {e}")

    async def derive_drift_vault_address(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Derives the Drift vault address from a given name.

        Args:
            name (str): Vault name.

        Returns:
            dict: Derived vault address.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.derive_drift_vault_address(self, name)
        except Exception as e:
            raise AgentKitError(f"Failed to derive Drift vault address: {e}")

    async def trade_using_delegated_drift_vault(
        self,
        vault: str,
        amount: float,
        symbol: str,
        action: str,
        trade_type: str,
        price: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Executes a trade using a delegated Drift vault.

        Args:
            vault (str): Vault address.
            amount (float): Trade amount.
            symbol (str): Market symbol.
            action (str): "long" or "short".
            trade_type (str): "market" or "limit".
            price (float, optional): Trade execution price.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_drift import DriftManager

            return await DriftManager.trade_using_delegated_drift_vault(
                self, vault, amount, symbol, action, trade_type, price
            )
        except Exception as e:
            raise AgentKitError(f"Failed to trade using delegated Drift vault: {e}")

    async def flash_open_trade(
        self, token: str, side: str, collateral_usd: float, leverage: float
    ) -> Optional[Dict[str, Any]]:
        """
        Opens a flash trade using the agent toolkit API.

        Args:
            token (str): The trading token.
            side (str): The trade direction ("buy" or "sell").
            collateral_usd (float): The collateral amount in USD.
            leverage (float): The leverage multiplier.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_flash import FlashTradeManager

            return await FlashTradeManager.flash_open_trade(
                self, token, side, collateral_usd, leverage
            )
        except Exception as e:
            raise AgentKitError(f"Failed to open flash trade: {e}")

    async def flash_close_trade(
        self, token: str, side: str
    ) -> Optional[Dict[str, Any]]:
        """
        Closes a flash trade using the agent toolkit API.

        Args:
            token (str): The trading token.
            side (str): The trade direction ("buy" or "sell").

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_flash import FlashTradeManager

            return await FlashTradeManager.flash_close_trade(self, token, side)
        except Exception as e:
            raise AgentKitError(f"Failed to close flash trade: {e}")

    async def resolve_all_domains(self, domain: str) -> Optional[str]:
        """
        Resolves all domain types for a given domain.

        Args:
            domain (str): The domain name.

        Returns:
            Optional[str]: The resolved domain's TLD.
        """
        try:
            from agentipy.tools.use_alldomains import AllDomainsManager

            return await AllDomainsManager.resolve_all_domains(self, domain)
        except Exception as e:
            raise AgentKitError(f"Failed to resolve all domains: {e}")

    async def get_owned_domains_for_tld(self, tld: str) -> Optional[List[str]]:
        """
        Retrieves domains owned by the user for a given TLD.

        Args:
            tld (str): The top-level domain.

        Returns:
            Optional[List[str]]: List of owned domains.
        """
        try:
            from agentipy.tools.use_alldomains import AllDomainsManager

            return await AllDomainsManager.get_owned_domains_for_tld(self, tld)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch owned domains: {e}")

    async def get_all_domains_tlds(self) -> Optional[List[str]]:
        """
        Retrieves all available TLDs.

        Returns:
            Optional[List[str]]: List of available TLDs.
        """
        try:
            from agentipy.tools.use_alldomains import AllDomainsManager

            return await AllDomainsManager.get_all_domains_tlds(self)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch all domains TLDs: {e}")

    async def get_owned_all_domains(self, owner: str) -> Optional[List[str]]:
        """
        Retrieves all domains owned by a given user.

        Args:
            owner (str): The owner's public key.

        Returns:
            Optional[List[str]]: List of owned domains.
        """
        try:
            from agentipy.tools.use_alldomains import AllDomainsManager

            return await AllDomainsManager.get_owned_all_domains(self, owner)
        except Exception as e:
            raise AgentKitError(f"Failed to fetch owned all domains: {e}")

    async def send_compressed_airdrop(
        self,
        mint_address: str,
        amount: float,
        decimals: int,
        recipients: List[str],
        priority_fee_in_lamports: int,
        should_log: Optional[bool] = False,
    ) -> Optional[List[str]]:
        try:
            from agentipy.tools.use_lightprotocol import LightProtocolManager

            return await LightProtocolManager.send_compressed_airdrop(
                self,
                mint_address,
                amount,
                decimals,
                recipients,
                priority_fee_in_lamports,
                should_log,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to fetch owned all domains: {e}")

    async def create_manifest_market(
        self,
        base_mint: str,
        quote_mint: str,
    ) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_manifest import ManifestManager

            return await ManifestManager.create_market(self, base_mint, quote_mint)
        except Exception as e:
            raise AgentKitError(f"Failed to create manifest market: {e}")

    async def place_limit_order(
        self,
        market_id: str,
        quantity: float,
        side: str,
        price: float,
    ) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_manifest import ManifestManager

            return await ManifestManager.place_batch_orders(
                self, market_id, quantity, side, price
            )
        except Exception as e:
            raise AgentKitError(f"Failed to place limit order: {e}")

    async def place_batch_orders(
        self,
        market_id: str,
        orders: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_manifest import ManifestManager

            return await ManifestManager.place_batch_orders(self, market_id, orders)
        except Exception as e:
            raise AgentKitError(f"Failed to place batch orders: {e}")

    async def cancel_all_orders(
        self,
        market_id: str,
    ) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_manifest import ManifestManager

            return await ManifestManager.cancel_all_orders(self, market_id)
        except Exception as e:
            raise AgentKitError(f"Failed to cancel all orders: {e}")

    async def withdraw_all(
        self,
        market_id: str,
    ) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_manifest import ManifestManager

            return await ManifestManager.withdraw_all(self, market_id)
        except Exception as e:
            raise AgentKitError(f"Failed to withdraw all: {e}")

    async def create_openbook_market(
        self,
        base_mint: str,
        quote_mint: str,
        lot_size: Optional[float] = 1,
        tick_size: Optional[float] = 0.01,
    ) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_openpook import OpenBookManager

            return await OpenBookManager.create_market(
                self, base_mint, quote_mint, lot_size, tick_size
            )
        except Exception as e:
            raise AgentKitError(f"Failed to create openbook market: {e}")

    async def close_position(
        self,
        position_mint_address: str,
    ) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_orca import OrcaManager

            return await OrcaManager.close_position(self, position_mint_address)
        except Exception as e:
            raise AgentKitError(f"Failed to close position: {e}")

    async def create_clmm(
        self,
        mint_deploy: str,
        mint_pair: str,
        initial_price: float,
        fee_tier: str,
    ) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_orca import OrcaManager

            return await OrcaManager.close_position(
                self, mint_deploy, mint_pair, initial_price, fee_tier
            )
        except Exception as e:
            raise AgentKitError(f"Failed to create clmm: {e}")

    async def create_liquidity_pool(
        self,
        deposit_token_amount: float,
        deposit_token_mint: str,
        other_token_mint: str,
        initial_price: float,
        max_price: float,
        fee_tier: str,
    ) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_orca import OrcaManager

            return await OrcaManager.create_liquidity_pool(
                self,
                deposit_token_amount,
                deposit_token_mint,
                other_token_mint,
                initial_price,
                max_price,
                fee_tier,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to create liquidity pool: {e}")

    async def fetch_positions(self) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_orca import OrcaManager

            return await OrcaManager.fetch_positions(self)
        except Exception as e:
            raise AgentKitError(f"Failed to close position: {e}")

    async def open_centered_position(
        self,
        whirlpool_address: str,
        price_offset_bps: int,
        input_token_mint: str,
        input_amount: float,
    ) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_orca import OrcaManager

            return await OrcaManager.open_centered_position(
                self,
                whirlpool_address,
                price_offset_bps,
                input_token_mint,
                input_amount,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to open centered position: {e}")

    async def open_single_sided_position(
        self,
        whirlpool_address: str,
        distance_from_current_price_bps: int,
        width_bps: int,
        input_token_mint: str,
        input_amount: float,
    ) -> Optional[Dict[str, Any]]:
        try:
            from agentipy.tools.use_orca import OrcaManager

            return await OrcaManager.open_single_sided_position(
                self,
                whirlpool_address,
                distance_from_current_price_bps,
                width_bps,
                input_token_mint,
                input_amount,
            )
        except Exception as e:
            raise AgentKitError(f"Failed to open single sided position: {e}")

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

    async def fluxbeam_create_pool(
        self,
        token_a: Pubkey,
        token_a_amount: float,
        token_b: Pubkey,
        token_b_amount: float,
    ) -> str:
        """
        Create a new pool using FluxBeam.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            token_a (Pubkey): Token mint address of the first token.
            token_a_amount (float): Amount to swap (in token decimals).
            token_b (Pubkey): Token mint address of the second token.
            token_b_amount (float): Amount to swap (in token decimals).

        Returns:
            str: Transaction signature.
        """
        from agentipy.tools.use_fluxbeam import FluxBeamManager

        try:
            return await FluxBeamManager.fluxbeam_create_pool(
                self, token_a, token_a_amount, token_b, token_b_amount
            )
        except Exception as e:
            raise AgentKitError(f"Failed to create pool using FluxBeam: {e}")

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

    async def restake(self, amount: float):
        """
        Restake all rewards.

        :return: A dictionary containing the transaction signature.
        """
        from agentipy.tools.use_solayer import SolayerManager

        try:
            return await SolayerManager.stake_with_solayer(self, amount)
        except Exception as e:
            raise AgentKitError(f"Failed to restake all rewards: {e}")

    async def rock_paper_scissors(self, amount: float, choice: str):
        """
        Play rock-paper-scissors with the Solana agent.

        :param choice: The player's choice ("rock", "paper", or "scissors").
        :param amount: The amount of SOL to stake.
        :return: A dictionary containing the game result.
        """
        from agentipy.tools.use_sendarcade import SendArcadeManager

        try:
            return await SendArcadeManager.rock_paper_scissor(self, amount, choice)
        except Exception as e:
            raise AgentKitError(f"Failed to play rock-paper-scissors: {e}")

    def close_accounts(
        self,
        mints: List[str],
    ) -> Optional[Dict[str, Any]]:
        """
        Close accounts for a given list of mints.

        Args:
            mints (List[str]): List of mint addresses.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_solutiofi import SolutiofiManager

            return SolutiofiManager.close_accounts(self, mints)
        except Exception as e:
            raise AgentKitError(f"Failed to close accounts: {e}")

    def burn_tokens(
        self,
        mints: List[str],
    ) -> Optional[Dict[str, Any]]:
        """
        Burn tokens for a given list of mints.

        Args:
            mints (List[str]): List of mint addresses.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_solutiofi import SolutiofiManager

            return SolutiofiManager.burn_tokens(self, mints)
        except Exception as e:
            raise AgentKitError(f"Failed to burn tokens: {e}")

    def merge_tokens(
        self,
        input_assets: List[Dict[str, Any]],
        output_mint: str,
        priority_fee: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Merge tokens for a given list of mints.

        Args:
            input_assets (List[Dict[str, Any]]): List of input assets.
            output_mint (str): Output mint address.
            priority_fee (str): Priority fee.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_solutiofi import SolutiofiManager

            return SolutiofiManager.merge_tokens(
                self, input_assets, output_mint, priority_fee
            )
        except Exception as e:
            raise AgentKitError(f"Failed to merge tokens: {e}")

    def spread_token(
        self,
        input_asset: Dict[str, Any],
        target_tokens: List[Dict[str, Any]],
        priority_fee: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Spread token for a given list of mints.

        Args:
            input_asset (Dict[str, Any]): Input asset.
            target_tokens (List[Dict[str, Any]]): List of target tokens.
            priority_fee (str): Priority fee.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_solutiofi import SolutiofiManager

            return SolutiofiManager.spread_token(
                self, input_asset, target_tokens, priority_fee
            )
        except Exception as e:
            raise AgentKitError(f"Failed to spread token: {e}")

    def approve_multisig_proposal(
        self,
        transaction_index: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Approve a multisig proposal.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            transaction_index (int): The transaction index.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_squads import SquadsManager

            return SquadsManager.approve_multisig_proposal(self, transaction_index)
        except Exception as e:
            raise AgentKitError(f"Failed to approve multisig proposal: {e}")

    def create_squads_multisig(
        self,
        creator: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Create a Squads multisig wallet.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            creator (str): The creator's public key.

        Returns:
            dict: Multisig wallet details.
        """
        try:
            from agentipy.tools.use_squads import SquadsManager

            return SquadsManager.create_squads_multisig(self, creator)
        except Exception as e:
            raise AgentKitError(f"Failed to create Squads multisig wallet: {e}")

    def create_multisig_proposal(
        self,
        transaction_index: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Create a multisig proposal.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            transaction_index (int): The transaction index.

        Returns:
            dict: Proposal details.
        """
        try:
            from agentipy.tools.use_squads import SquadsManager

            return SquadsManager.create_multisig_proposal(self, transaction_index)
        except Exception as e:
            raise AgentKitError(f"Failed to create multisig proposal: {e}")

    def deposit_to_multisig_treasury(
        self,
        amount: float,
        vault_index: int,
        mint: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Deposit funds to a multisig treasury.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            amount (float): The amount to deposit.
            vault_index (int): The vault index.
            mint (str): The mint address.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_squads import SquadsManager

            return SquadsManager.deposit_to_multisig_treasury(
                self, amount, vault_index, mint
            )
        except Exception as e:
            raise AgentKitError(f"Failed to deposit to multisig treasury: {e}")

    def execute_multisig_proposal(
        self,
        transaction_index: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Execute a multisig proposal.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            transaction_index (int): The transaction index.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_squads import SquadsManager

            return SquadsManager.execute_multisig_proposal(self, transaction_index)
        except Exception as e:
            raise AgentKitError(f"Failed to execute multisig proposal: {e}")

    def reject_multisig_proposal(
        self,
        transaction_index: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Reject a multisig proposal.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            transaction_index (int): The transaction index.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_squads import SquadsManager

            return SquadsManager.reject_multisig_proposal(self, transaction_index)
        except Exception as e:
            raise AgentKitError(f"Failed to reject multisig proposal: {e}")

    def transfer_from_multisig_treasury(
        self,
        amount: float,
        to: str,
        vault_index: int,
        mint: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Transfer funds from a multisig treasury.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            amount (float): The amount to transfer.
            to (str): The recipient's public key.
            vault_index (int): The vault index.
            mint (str): The mint address.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_squads import SquadsManager

            return SquadsManager.transfer_from_multisig_treasury(
                self, amount, to, vault_index, mint
            )
        except Exception as e:
            raise AgentKitError(f"Failed to transfer from multisig treasury: {e}")

    def simulate_switchboard_feed(
        self,
        feed: str,
        crossbar_url: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Simulate a Switchboard feed.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            feed (str): The feed name.
            crossbar_url (str): The Crossbar URL.

        Returns:
            dict: Simulation details.
        """
        try:
            from agentipy.tools.use_switchboard import SwitchboardManager

            return SwitchboardManager.simulate_switchboard_feed(
                self, feed, crossbar_url
            )
        except Exception as e:
            raise AgentKitError(f"Failed to simulate Switchboard feed: {e}")

    def list_nft_for_sale(
        self,
        price: float,
        nft_mint: str,
    ) -> Optional[Dict[str, Any]]:
        """
        List an NFT for sale.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            price (float): The sale price.
            nft_mint (str): The NFT mint address.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_tensor import TensorManager

            return TensorManager.list_nft_for_sale(self, price, nft_mint)
        except Exception as e:
            raise AgentKitError(f"Failed to list NFT for sale: {e}")

    def cancel_listing(
        self,
        nft_mint: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Cancel an NFT listing.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            nft_mint (str): The NFT mint address.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_tensor import TensorManager

            return TensorManager.cancel_listing(self, nft_mint)
        except Exception as e:
            raise AgentKitError(f"Failed to cancel listing: {e}")

    def create_tiplink(
        self,
        amount: float,
        spl_mint_address: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Create a TipLink.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            amount (float): The tip amount.
            spl_mint_address (str): The SPL mint address.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_tiplink import TiplinkManager

            return TiplinkManager.create_tiplink(self, amount, spl_mint_address)
        except Exception as e:
            raise AgentKitError(f"Failed to create TipLink: {e}")

    def deposit_strategy(
        self,
        deposit_amount: str,
        vault: str,
        strategy: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Deposit funds to a strategy.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            deposit_amount (str): The deposit amount.
            vault (str): The vault address.
            strategy (str): The strategy address.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_voltr import VoltrManager

            return VoltrManager.deposit_strategy(self, deposit_amount, vault, strategy)
        except Exception as e:
            raise AgentKitError(f"Failed to deposit to strategy: {e}")

    def get_position_values(self, vault: str) -> Optional[Dict[str, Any]]:
        """
        Get position values for a given vault.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            vault (str): The vault address.

        Returns:
            dict: Position values.
        """
        try:
            from agentipy.tools.use_voltr import VoltrManager

            return VoltrManager.get_position_values(self, vault)
        except Exception as e:
            raise AgentKitError(f"Failed to get position values: {e}")

    def withdraw_strategy(
        self,
        withdraw_amount: str,
        vault: str,
        strategy: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Withdraw funds from a strategy.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            withdraw_amount (str): The withdrawal amount.
            vault (str): The vault address.
            strategy (str): The strategy address.

        Returns:
            dict: Transaction details.
        """
        try:
            from agentipy.tools.use_voltr import VoltrManager

            return VoltrManager.withdraw_strategy(
                self, withdraw_amount, vault, strategy
            )
        except Exception as e:
            raise AgentKitError(f"Failed to withdraw from strategy: {e}")

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
        from agentipy.tools.use_virtuals import VirtualsManager

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
        from agentipy.tools.use_virtuals import VirtualsManager

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
        from agentipy.tools.use_virtuals import VirtualsManager

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
        from agentipy.tools.use_virtuals import VirtualsManager

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
        from agentipy.tools.use_virtuals import VirtualsManager

        try:
            return VirtualsManager.sell_prototype(
                self, token_address, amount, builder_id, slippage
            )
        except Exception as e:
            raise AgentKitError(f"Failed to sell Prototype tokens: {e}")
