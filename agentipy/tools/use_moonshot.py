import logging
import struct

from solana.rpc.api import Client
from solana.rpc.types import TokenAccountOpts, TxOpts
from solders.instruction import AccountMeta  # type: ignore
from solders.compute_budget import set_compute_unit_limit  # type: ignore
from solders.compute_budget import set_compute_unit_price  # type: ignore
from solders.instruction import Instruction  # type: ignore
from solders.message import MessageV0  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solders.transaction import VersionedTransaction  # type: ignore
from spl.token.instructions import (create_associated_token_account,
                                    get_associated_token_address)

from agentipy.agent import SolanaAgentKit
from agentipy.utils.moonshot.constants import *
from agentipy.utils.moonshot.curve import (TradeDirection,
                                           derive_curve_accounts,
                                           get_collateral_amount_by_tokens,
                                           get_tokens_by_collateral_amount)
from agentipy.utils.moonshot.utils import confirm_txn, get_token_balance

logger = logging.getLogger(__name__)
class MoonshotManager:
    @staticmethod
    def buy(agent:SolanaAgentKit, mint_str: str, collateral_amount: float = 0.01, slippage_bps: int = 500):
        try:
            client = Client(agent.rpc_url)
            amount = get_tokens_by_collateral_amount(mint_str, collateral_amount, TradeDirection.BUY)
            
            collateral_amount = int(collateral_amount * LAMPORTS_PER_SOL)

            logger.info(f"Collateral Amount (in lamports): {collateral_amount}, Amount: {amount}, Slippage (bps): {slippage_bps}")
            
            if not amount:
                logger.error("Failed to get tokens by collateral amount...", exc_info=True)
                return

            SENDER = agent.wallet_address
            MINT = Pubkey.from_string(mint_str)
            
            token_account, token_account_instructions = None, None
            try:
                account_data = agent.connection.get_token_accounts_by_owner(SENDER, TokenAccountOpts(MINT))
                token_account = account_data.value[0].pubkey
                token_account_instructions = None
            except:
                token_account = get_associated_token_address(SENDER, MINT)
                token_account_instructions = create_associated_token_account(SENDER, SENDER, MINT)

            CURVE_ACCOUNT, CURVE_TOKEN_ACCOUNT = derive_curve_accounts(MINT)
            SENDER_TOKEN_ACCOUNT = token_account

            keys = [
                AccountMeta(pubkey=SENDER, is_signer=True, is_writable=True),
                AccountMeta(pubkey=SENDER_TOKEN_ACCOUNT, is_signer=False, is_writable=True),
                AccountMeta(pubkey=CURVE_ACCOUNT, is_signer=False, is_writable=True),
                AccountMeta(pubkey=CURVE_TOKEN_ACCOUNT, is_signer=False, is_writable=True),
                AccountMeta(pubkey=DEX_FEE, is_signer=False, is_writable=True),
                AccountMeta(pubkey=HELIO_FEE, is_signer=False, is_writable=True),
                AccountMeta(pubkey=MINT, is_signer=False, is_writable=True), 
                AccountMeta(pubkey=CONFIG_ACCOUNT, is_signer=False, is_writable=True),
                AccountMeta(pubkey=TOKEN_PROGRAM, is_signer=False, is_writable=True),
                AccountMeta(pubkey=ASSOC_TOKEN_ACC_PROG, is_signer=False, is_writable=False),
                AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False)
            ]

            discriminator_as_int = 16927863322537952870
            integers = [
                discriminator_as_int,
                amount,
                collateral_amount,
                slippage_bps
            ]
            
            binary_segments = [struct.pack('<Q', integer) for integer in integers]
            data = b''.join(binary_segments)  
            
            swap_instruction = Instruction(MOONSHOT_PROGRAM, data, keys)

            instructions = []
            instructions.append(set_compute_unit_price(UNIT_PRICE))
            instructions.append(set_compute_unit_limit(UNIT_BUDGET))
            
            if token_account_instructions:
                instructions.append(token_account_instructions)
            
            instructions.append(swap_instruction)

            compiled_message = MessageV0.try_compile(
                agent.wallet_address,
                instructions,
                [],  
                client.get_latest_blockhash().value.blockhash,
            )

            transaction = VersionedTransaction(compiled_message, [agent.wallet])
            
            txn_sig = client.send_transaction(transaction, opts=TxOpts(skip_preflight=True, preflight_commitment="confirmed")).value
            logger.info(f"Transaction Signature: {txn_sig}")
            
            confirm = confirm_txn(txn_sig)
            logger.info(f"Transaction Confirmation: {confirm}")
        except Exception as e:
            logger.error(e, exc_info=True)
    
    @staticmethod 
    def sell(agent:SolanaAgentKit, mint_str: str, token_balance: float=None, slippage_bps: int=500):
        try:
            client = Client(agent.rpc_url)
            if token_balance is None:
                token_balance = get_token_balance(PUB_KEY, mint_str)
            
            logger.info(f"Token Balance: {token_balance}")
            
            if token_balance == 0:
                return
            
            collateral_amount = get_collateral_amount_by_tokens(mint_str, token_balance, TradeDirection.SELL)
            amount = int(token_balance * LAMPORTS_PER_SOL)
            
            logger.info(f"Collateral Amount: {collateral_amount}, Amount (in lamports): {amount}, Slippage (bps): {slippage_bps}")
            
            MINT = Pubkey.from_string(mint_str)
            CURVE_ACCOUNT, CURVE_TOKEN_ACCOUNT = derive_curve_accounts(MINT)
            SENDER = agent.wallet_address
            SENDER_TOKEN_ACCOUNT = get_associated_token_address(SENDER, MINT)

            keys = [
                AccountMeta(pubkey=SENDER, is_signer=True, is_writable=True),
                AccountMeta(pubkey=SENDER_TOKEN_ACCOUNT, is_signer=False, is_writable=True),
                AccountMeta(pubkey=CURVE_ACCOUNT, is_signer=False, is_writable=True),
                AccountMeta(pubkey=CURVE_TOKEN_ACCOUNT, is_signer=False, is_writable=True),
                AccountMeta(pubkey=DEX_FEE, is_signer=False, is_writable=True),
                AccountMeta(pubkey=HELIO_FEE, is_signer=False, is_writable=True),
                AccountMeta(pubkey=MINT, is_signer=False, is_writable=True), 
                AccountMeta(pubkey=CONFIG_ACCOUNT, is_signer=False, is_writable=True),
                AccountMeta(pubkey=TOKEN_PROGRAM, is_signer=False, is_writable=True),
                AccountMeta(pubkey=ASSOC_TOKEN_ACC_PROG, is_signer=False, is_writable=False),
                AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False)
            ]

            discriminator_as_int = 12502976635542562355
            integers = [
                discriminator_as_int,
                amount,
                collateral_amount,
                slippage_bps
            ]
            
            binary_segments = [struct.pack('<Q', integer) for integer in integers]
            data = b''.join(binary_segments)  
            
            swap_instruction = Instruction(MOONSHOT_PROGRAM, data, keys)

            instructions = []
            instructions.append(set_compute_unit_price(UNIT_PRICE))
            instructions.append(set_compute_unit_limit(UNIT_BUDGET))
            instructions.append(swap_instruction)

            compiled_message = MessageV0.try_compile(
                agent.wallet_address,
                instructions,
                [],  
                client.get_latest_blockhash().value.blockhash,
            )

            transaction = VersionedTransaction(compiled_message, [agent.wallet])
            
            txn_sig = client.send_transaction(transaction, opts=TxOpts(skip_preflight=True, preflight_commitment="confirmed")).value
            logger.info(f"Transaction Signature: {txn_sig}")

            confirm = confirm_txn(txn_sig)
            logger.info(f"Transaction Confirmation: {confirm}")
        except Exception as e:
            logger.error(e, exc_info=True)