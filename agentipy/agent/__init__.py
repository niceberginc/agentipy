import logging
import os
from typing import List, Optional

import base58
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from typing_extensions import Union

from agentipy.constants import BASE_PROXY_URL, DEFAULT_OPTIONS
from agentipy.types import BondingCurveState, PumpfunTokenOptions
from agentipy.utils.meteora_dlmm.types import ActivationType
from agentipy.wallet.solana_wallet_client import SolanaWalletClient

logger = logging.getLogger(__name__)


class SolanaAgentKitError(Exception):
    """Custom exception for errors in SolanaAgentKit"""
    pass


class SolanaAgentKit:
    """
    Main class for interacting with the Solana blockchain.

    Attributes:
        connection (AsyncClient): Solana RPC connection.
        wallet (SolanaWalletClient): Wallet client for signing and sending transactions.
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
        generate_wallet: bool = False,
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
            generate_wallet (bool): If True, generates a new wallet and returns the details.
        """
        self.rpc_url = rpc_url or os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY", "")
        self.helius_api_key = helius_api_key or os.getenv("HELIUS_API_KEY", "")
        self.helius_rpc_url = helius_rpc_url or os.getenv("HELIUS_RPC_URL", "")
        self.backpack_api_key = backpack_api_key or os.getenv("BACKPACK_API_KEY", "")
        self.backpack_api_secret = backpack_api_secret or os.getenv("BACKPACK_API_SECRET", "")
        self.quicknode_rpc_url = quicknode_rpc_url or os.getenv("QUICKNODE_RPC_URL", "")
        self.jito_block_engine_url = jito_block_engine_url or os.getenv("JITO_BLOCK_ENGINE_URL", "")
        self.jito_uuid = jito_uuid or os.getenv("JITO_UUID", None)

        if generate_wallet:
            self.wallet = Keypair()
            self.wallet_address = self.wallet.pubkey()
            self.private_key = base58.b58encode(self.wallet.secret()).decode("utf-8")
        else:
            self.private_key = private_key or os.getenv("SOLANA_PRIVATE_KEY", "")
            self.wallet = Keypair.from_base58_string(self.private_key)
            self.wallet_address = self.wallet.pubkey()

        if not self.wallet or not self.wallet_address:
            raise ValueError("A valid private key must be provided or a wallet must be generated.")

        self.connection = AsyncClient(self.rpc_url)
        self.connection_client = Client(self.rpc_url)

        self.wallet_client = SolanaWalletClient(self.connection_client, self.wallet)

        if generate_wallet:
            logger.info("New Wallet Generated:")
            logger.info(f"Public Key: {self.wallet_address}")
            logger.info(f"Private Key: {self.private_key}")

    async def request_faucet_funds(self):
        from agentipy.tools.request_faucet_funds import FaucetManager
        try:
            return await FaucetManager.request_faucet_funds(self)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to request faucet funds: {e}")

    async def deploy_token(self, decimals: int = DEFAULT_OPTIONS["TOKEN_DECIMALS"]):
        from agentipy.tools.deploy_token import TokenDeploymentManager
        try:
            return await TokenDeploymentManager.deploy_token(self, decimals)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to deploy token: {e}")

    async def get_balance(self, token_address: Optional[Pubkey] = None):
        from agentipy.tools.get_balance import BalanceFetcher
        try:
            return await BalanceFetcher.get_balance(self, token_address)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch balance: {e}")
    
    async def fetch_price(self, token_id: str):
        from agentipy.tools.fetch_price import TokenPriceFetcher
        try:
            return await TokenPriceFetcher.fetch_price(token_id)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch price: {e}")

    async def transfer(self, to: str, amount: float, mint: Optional[Pubkey] = None):
        from agentipy.tools.transfer import TokenTransferManager
        try:
            return await TokenTransferManager.transfer(self, to, amount, mint)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to execute transfer: {e}")

    async def trade(self, output_mint: Pubkey, input_amount: float, input_mint: Optional[Pubkey] = None, slippage_bps: int = DEFAULT_OPTIONS["SLIPPAGE_BPS"]):
        from agentipy.tools.trade import TradeManager
        try:
            return await TradeManager.trade(self, output_mint, input_amount, input_mint, slippage_bps)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to trade: {e}")

    async def lend_assets(self, amount: float):
        from agentipy.tools.lend import AssetLender
        try:
            return await AssetLender.lend_asset(self, amount)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to lend asset: {e}")

    async def get_tps(self):
        from agentipy.tools.get_tps import SolanaPerformanceTracker
        try:
            return await SolanaPerformanceTracker.fetch_current_tps(self)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch tps: {e}")
    
    async def get_token_data_by_ticker(self, ticker: str):
        from agentipy.tools.get_token_data import TokenDataManager
        try:
            return TokenDataManager.get_token_data_by_ticker(ticker)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to get token data: {e}")
    
    async def get_token_data_by_address(self, mint: str):
        from agentipy.tools.get_token_data import TokenDataManager
        try: 
            return TokenDataManager.get_token_data_by_address(Pubkey.from_string(mint))
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to get token data: {e}")

    async def launch_pump_fun_token(self, token_name: str, token_ticker: str, description: str, image_url: str, options: Optional[PumpfunTokenOptions] = None):
        from agentipy.tools.launch_pumpfun_token import PumpfunTokenManager
        try:
            return await PumpfunTokenManager.launch_pumpfun_token(self, token_name, token_ticker, description, image_url, options)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to launch token on pumpfun: {e}")

    async def stake(self, amount: int):
        from agentipy.tools.stake_with_jup import StakeManager
        try:
            return await StakeManager.stake_with_jup(self, amount)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to stake: {e}")
    
    async def create_meteora_dlmm_pool(self, bin_step: int, token_a_mint: Pubkey, token_b_mint: Pubkey, initial_price: float, price_rounding_up: bool, fee_bps: int, activation_type: ActivationType, has_alpha_vault: bool, activation_point: Optional[int]):
        from agentipy.tools.create_meteora_dlmm_pool import MeteoraManager
        try:
            return await MeteoraManager.create_meteora_dlmm_pool(self, bin_step, token_a_mint, token_b_mint, initial_price, price_rounding_up, fee_bps, activation_type, has_alpha_vault, activation_point)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to create dlmm pool: {e}")
    
    async def buy_with_raydium(self, pair_address: str, sol_in: float = 0.01, slippage: int = 5):
        from agentipy.tools.use_raydium import RaydiumManager
        try:
            return await RaydiumManager.buy_with_raydium(self, pair_address, sol_in, slippage)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to buy using raydium: {e}")
    
    async def sell_with_raydium(self, pair_address: str, percentage: int = 100, slippage: int = 5):
        from agentipy.tools.use_raydium import RaydiumManager
        try:
            return await RaydiumManager.sell_with_raydium(self, pair_address, percentage, slippage)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to sell using raydium: {e}")
    
    async def burn_and_close_accounts(self, token_account: str):
        from agentipy.tools.burn_and_close_account import BurnManager
        try:
            return await BurnManager.burn_and_close_account(self, token_account)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to close account: {e}")
    
    async def multiple_burn_and_close_accounts(self, token_accounts: list[str]):
        from agentipy.tools.burn_and_close_account import BurnManager
        try:
            return await BurnManager.process_multiple_accounts(self, token_accounts)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to close accounts: {e}")
    
    async def create_gibwork_task(self, title: str, content: str, requirements: str, tags: list[str], token_mint_address: Pubkey, token_amount: int):
        from agentipy.tools.create_gibwork import GibworkManager
        try:
            return await GibworkManager.create_gibwork_task(self, title, content, requirements, tags, token_mint_address, token_amount)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to create task: {e}")
    
    async def buy_using_moonshot(self, mint_str: str, collateral_amount: float = 0.01, slippage_bps: int = 500):
        from agentipy.tools.use_moonshot import MoonshotManager
        try:
            return await MoonshotManager.buy(self, mint_str, collateral_amount, slippage_bps)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to buy using moonshot: {e}")
    
    async def sell_using_moonshot(self, mint_str: str, token_balance: float = 0.01, slippage_bps: int = 500):
        from agentipy.tools.use_moonshot import MoonshotManager
        try:
            return await MoonshotManager.sell(self, mint_str, token_balance, slippage_bps)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to sell using moonshot: {e}")
    
    async def pyth_fetch_price(self, mint_str: str):
        from agentipy.tools.use_pyth import PythManager
        try:
            return await PythManager.get_price(mint_str)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
    
    async def stork_fetch_price(self, asset_id: str):
        from agentipy.tools.use_stork import StorkManager
        try:
            return await StorkManager.get_price(self, asset_id)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_balances(self, address: str):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_balances(self, address)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")

    async def get_address_name(self, address: str):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_address_name(self, address)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_nft_events(self, accounts: List[str],
            types: List[str] = None,
            sources: List[str] = None,
            start_slot: int = None,
            end_slot: int = None,
            start_time: int = None,
            end_time: int = None,
            first_verified_creator: List[str] = None,
            verified_collection_address: List[str] = None,
            limit : int = None,
            sort_order: str = None,
            pagination_token: str = None):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_nft_events(self, accounts,types,sources,start_slot,end_slot,start_time,end_time,first_verified_creator,verified_collection_address,limit,sort_order,pagination_token)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_mintlists(self, first_verified_creators: List[str],
        verified_collection_addresses: List[str]=None,
        limit: int=None,
        pagination_token: str=None):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_mintlists(self,first_verified_creators,verified_collection_addresses,limit,pagination_token)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_nft_fingerprint(self, mints: List[str]):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_nft_fingerprint(self,mints)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_active_listings(self, first_verified_creators: List[str],
        verified_collection_addresses: List[str]=None,
        marketplaces: List[str]=None,
        limit: int=None,
        pagination_token: str=None):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_active_listings(self,first_verified_creators,verified_collection_addresses,marketplaces,limit,pagination_token)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_nft_metadata(self, mint_accounts: List[str]):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_nft_metadata(self,mint_accounts)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_raw_transactions(self,
        accounts: List[str], 
        start_slot: int=None,
        end_slot: int=None,
        start_time: int=None,
        end_time: int=None,
        limit: int=None,
        sort_order: str=None,
        pagination_token: str=None):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_raw_transactions(self,accounts,start_slot,end_slot,start_time,end_time,limit,sort_order,pagination_token)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_parsed_transactions(self, transactions: List[str], commitment: str=None):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_parsed_transactions(self,transactions,commitment)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
    
    async def get_parsed_transaction_history(self,
        address: str, 
        before: str='', 
        until: str='', 
        commitment: str='',
        source: str='',
        type: str=''):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_parsed_transaction_history(self,address,before,until,commitment,source,type)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def create_webhook(self, 
        webhook_url: str, 
        transaction_types: list, 
        account_addresses: list, 
        webhook_type: str, 
        txn_status: str="all",
        auth_header: str=None):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.create_webhook(self,webhook_url,transaction_types,account_addresses,webhook_type,txn_status,auth_header)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_all_webhooks(self):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_all_webhooks(self)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_webhook(self, webhook_id: str):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.get_webhook(self,webhook_id)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def edit_webhook(self,
        webhook_id: str, 
        webhook_url: str, 
        transaction_types: list, 
        account_addresses: list, 
        webhook_type: str, 
        txn_status: str="all",
        auth_header: str=None):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.edit_webhook(self,webhook_id,webhook_url,transaction_types,account_addresses,webhook_type,txn_status,auth_header)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")

    async def delete_webhook(self, webhook_id: str):
        from agentipy.tools.use_helius import HeliusManager
        try:
            return HeliusManager.delete_webhook(self,webhook_id)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def fetch_token_report_summary(mint:str):
        from agentipy.tools.rugcheck import RugCheckManager
        try:
            return RugCheckManager.fetch_token_report_summary(mint)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def fetch_token_detailed_report(mint:str):
        from agentipy.tools.rugcheck import RugCheckManager
        try:
            return RugCheckManager.fetch_token_detailed_report(mint)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_pump_curve_state(conn: AsyncClient, curve_address: Pubkey,):
        from agentipy.tools.use_pumpfun import PumpfunManager
        try:
            return PumpfunManager.get_pump_curve_state(conn, curve_address)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def calculate_pump_curve_price(curve_state:BondingCurveState):
        from agentipy.tools.use_pumpfun import PumpfunManager
        try:
            return PumpfunManager.calculate_pump_curve_price(curve_state)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def buy_token(self, mint:Pubkey, bonding_curve:Pubkey,associated_bonding_curve:Pubkey, amount:float, slippage:float,max_retries:int):
        from agentipy.tools.use_pumpfun import PumpfunManager
        try:
            return PumpfunManager.buy_token(self,mint,bonding_curve,associated_bonding_curve,amount,slippage,max_retries)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")

    async def sell_token(self, mint:Pubkey, bonding_curve:Pubkey,associated_bonding_curve:Pubkey, amount:float, slippage:float,max_retries:int):
        from agentipy.tools.use_pumpfun import PumpfunManager
        try:
            return PumpfunManager.sell_token(self, mint, bonding_curve, associated_bonding_curve, slippage, max_retries)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")

    async def resolve_name_to_address(self, domain: str):
        from agentipy.tools.use_sns import NameServiceManager
        try:
            return NameServiceManager.resolve_name_to_address(self, domain)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_favourite_domain(self, owner: str):
        from agentipy.tools.use_sns import NameServiceManager
        try:
            return NameServiceManager.get_favourite_domain(self, owner)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_all_domains_for_owner(self, owner: str):
        from agentipy.tools.use_sns import NameServiceManager
        try:
            return NameServiceManager.get_all_domains_for_owner(self, owner)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_registration_transaction(self, domain: str, buyer: str, buyer_token_account: str, space: int, 
                                     mint: Optional[str] = None, referrer_key: Optional[str] = None):
        from agentipy.tools.use_sns import NameServiceManager
        try:
            return NameServiceManager.get_registration_transaction(self, domain, buyer, buyer_token_account, space, mint, referrer_key)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")

    async def deploy_collection(self, name: str, uri: str, royalty_basis_points: int, creator_address: str):
        from agentipy.tools.use_metaplex import DeployCollectionManager
        try:
            return DeployCollectionManager.deploy_collection(self, name, uri, royalty_basis_points, creator_address)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_metaplex_asset(self, assetId:str):
        from agentipy.tools.use_metaplex import DeployCollectionManager
        try:
            return DeployCollectionManager.get_metaplex_asset(self, assetId)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_metaplex_assets_by_creator(self,creator: str, onlyVerified: bool = False, sortBy: Union[str, None] = None,
    sortDirection: Union[str, None] = None,
    limit: Union[int, None] = None,
    page: Union[int, None] = None,
    before: Union[str, None] = None,
    after: Union[str, None] = None):
        from agentipy.tools.use_metaplex import DeployCollectionManager
        try:
            return DeployCollectionManager.get_metaplex_assets_by_creator(self, creator, onlyVerified, sortBy, sortDirection, limit, page, before, after)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_metaplex_assets_by_authority(self,authority: str, sortBy: Union[str, None] = None,
    sortDirection: Union[str, None] = None,
    limit: Union[int, None] = None,
    page: Union[int, None] = None,
    before: Union[str, None] = None,
    after: Union[str, None] = None):
        from agentipy.tools.use_metaplex import DeployCollectionManager
        try:
            return DeployCollectionManager.get_metaplex_assets_by_authority(self, authority, sortBy, sortDirection, limit, page, before, after)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def mint_metaplex_core_nft(self,collectionMint: str, name: str, uri: str, sellerFeeBasisPoints: Union[int, None] = None, address: Union[str, None] = None,
    share: Union[str, None] = None, recipient: Union[str, None] = None):
        from agentipy.tools.use_metaplex import DeployCollectionManager
        try:
            return DeployCollectionManager.mint_metaplex_core_nft(self, collectionMint, name, uri, sellerFeeBasisPoints, address, share, recipient)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
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
    dst_chain_token_out_amount: str = "auto"):
        from agentipy.tools.use_debridge import DeBridgeManager   
        try:
            return DeBridgeManager.create_debridge_transaction(self, src_chain_id, src_chain_token_in, src_chain_token_in_amount, dst_chain_id, dst_chain_token_out, dst_chain_token_out_recipient, src_chain_order_authority_address, dst_chain_order_authority_address, affiliate_fee_percent, affiliate_fee_recipient, prepend_operating_expenses, dst_chain_token_out_amount)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def execute_debridge_transaction(self, transaction_data: dict):
        from agentipy.tools.use_debridge import DeBridgeManager   
        try:
            return await DeBridgeManager.execute_debridge_transaction(self, transaction_data)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def check_transaction_status(self, tx_hash: str):
        from agentipy.tools.use_debridge import DeBridgeManager   
        try:
            return await DeBridgeManager.check_transaction_status(self, tx_hash)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def cybers_create_coin(
        self, 
        name: str,
        symbol: str,
        image_path: str,
        tweet_author_id: str,
        tweet_author_username: str):
        from agentipy.tools.use_cybers import CybersManager   
        try:
            return CybersManager.create_coin(self, name, symbol, image_path, tweet_author_id, tweet_author_username)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")

    async def get_tip_accounts(self):
        from agentipy.tools.use_jito import JitoManager
        try:
            return JitoManager.get_tip_accounts(self)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")

    async def get_random_tip_account():
        from agentipy.tools.use_jito import JitoManager
        try:
            return JitoManager.get_random_tip_account()
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_bundle_statuses(self, bundle_uuids):
        from agentipy.tools.use_jito import JitoManager
        try:
            return JitoManager.get_bundle_statuses(self, bundle_uuids)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")

    async def send_bundle(self, params=None):
        from agentipy.tools.use_jito import JitoManager
        try:
            return JitoManager.send_bundle(self, params)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def get_inflight_bundle_statuses(self, bundle_uuids):
        from agentipy.tools.use_jito import JitoManager
        try:
            return JitoManager.get_inflight_bundle_statuses(self, bundle_uuids)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
        
    async def send_txn(self, params=None, bundleOnly=False):
        from agentipy.tools.use_jito import JitoManager
        try:
            return JitoManager.send_txn(self, params, bundleOnly)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to {e}")
    
    async def get_account_balances(self):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_account_balances(self)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch account balances: {e}")


    async def request_withdrawal(self, address: str, blockchain: str, quantity: str, symbol: str, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.request_withdrawal(self, address, blockchain, quantity, symbol, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to request withdrawal: {e}")


    async def get_account_settings(self):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_account_settings(self)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch account settings: {e}")


    async def update_account_settings(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.update_account_settings(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to update account settings: {e}")


    async def get_borrow_lend_positions(self):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_borrow_lend_positions(self)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch borrow/lend positions: {e}")


    async def execute_borrow_lend(self, quantity: str, side: str, symbol: str):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.execute_borrow_lend(self, quantity, side, symbol)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to execute borrow/lend operation: {e}")


    async def get_collateral_info(self, sub_account_id: int = None):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_collateral_info(self, sub_account_id)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch collateral information: {e}")


    async def get_account_deposits(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_account_deposits(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch account deposits: {e}")


    async def get_open_positions(self):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_open_positions(self)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch open positions: {e}")


    async def get_borrow_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_borrow_history(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch borrow history: {e}")


    async def get_interest_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_interest_history(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch interest history: {e}")


    async def get_fill_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_fill_history(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch fill history: {e}")


    async def get_borrow_position_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_borrow_position_history(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch borrow position history: {e}")


    async def get_funding_payments(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_funding_payments(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch funding payments: {e}")


    async def get_order_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_order_history(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch order history: {e}")


    async def get_pnl_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_pnl_history(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch PNL history: {e}")


    async def get_settlement_history(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_settlement_history(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch settlement history: {e}")


    async def get_users_open_orders(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_users_open_orders(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch user's open orders: {e}")


    async def execute_order(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.execute_order(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to execute order: {e}")


    async def cancel_open_order(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.cancel_open_order(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to cancel open order: {e}")


    async def get_open_orders(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_open_orders(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch open orders: {e}")


    async def cancel_open_orders(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.cancel_open_orders(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to cancel open orders: {e}")


    async def get_supported_assets(self):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_supported_assets(self)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch supported assets: {e}")


    async def get_ticker_information(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_ticker_information(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch ticker information: {e}")


    async def get_markets(self):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_markets(self)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch markets: {e}")


    async def get_market(self, **kwargs):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_market(self, **kwargs)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch market: {e}")


    async def get_tickers(self):
        from agentipy.tools.use_backpack import BackpackManager
        try:
            return await BackpackManager.get_tickers(self)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch tickers: {e}")
    
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
            raise SolanaAgentKitError(f"Failed to fetch order book depth: {e}")


    async def get_klines(self, symbol: str, interval: str, start_time: int, end_time: int = None):
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
            return await BackpackManager.get_klines(self, symbol, interval, start_time, end_time)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch K-Lines: {e}")


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
            raise SolanaAgentKitError(f"Failed to fetch mark price: {e}")


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
            raise SolanaAgentKitError(f"Failed to fetch open interest: {e}")


    async def get_funding_interval_rates(self, symbol: str, limit: int = 100, offset: int = 0):
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
            return await BackpackManager.get_funding_interval_rates(self, symbol, limit, offset)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch funding interval rates: {e}")


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
            raise SolanaAgentKitError(f"Failed to fetch system status: {e}")


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
            raise SolanaAgentKitError(f"Failed to send ping: {e}")


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
            raise SolanaAgentKitError(f"Failed to fetch system time: {e}")


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
            raise SolanaAgentKitError(f"Failed to fetch recent trades: {e}")


    async def get_historical_trades(self, symbol: str, limit: int = 100, offset: int = 0):
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
            return await BackpackManager.get_historical_trades(self, symbol, limit, offset)
        except Exception as e:
            raise SolanaAgentKitError(f"Failed to fetch historical trades: {e}")