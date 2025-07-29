import logging

from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solders.compute_budget import set_compute_unit_limit  # type: ignore
from solders.compute_budget import set_compute_unit_price  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
#from solana.transaction import Transaction
from solders.transaction import Transaction  # type: ignore
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import (BurnParams, CloseAccountParams, burn,
                                    close_account)

from agentipy.agent import SolanaAgentKit

# Configure logger for this module
logger = logging.getLogger(__name__)

class BurnValues:
    DEFAULT_COMPUTE_UNIT_PRICE = 100_000
    DEFAULT_COMPUTE_UNIT_LIMIT = 100_000

class BurnManager:
    @staticmethod
    def burn_and_close_account(agent: SolanaAgentKit, token_account: str):
        """
        Burns tokens and closes the given token account.

        Parameters:
        agent (SolanaAgentKit): The agent instance containing wallet and RPC configuration.
        token_account (str): The public key of the token account to process.
        """
        token_account_pubkey = Pubkey.from_string(token_account)
        try:
            client = Client(agent.rpc_url)
            token_balance = int(client.get_token_account_balance(token_account_pubkey).value.amount)
            logger.info(f"Token balance for {token_account}: {token_balance}")
        except Exception as e:
            logger.error(f"Error fetching token balance for {token_account}: {e}", exc_info=True)
            return

        owner = agent.wallet.pubkey()
        recent_blockhash = client.get_latest_blockhash().value.blockhash

        transaction = Transaction()
        transaction.fee_payer = owner
        transaction.recent_blockhash = recent_blockhash

        if token_balance > 0:
            try:
                mint_str = client.get_account_info_json_parsed(token_account_pubkey).value.data.parsed['info']['mint']
                mint = Pubkey.from_string(mint_str)
                burn_instruction = burn(
                    BurnParams(
                        program_id=TOKEN_PROGRAM_ID,
                        account=token_account_pubkey,
                        mint=mint,
                        owner=owner,
                        amount=token_balance
                    )
                )
                transaction.add(burn_instruction)
                logger.info(f"Prepared burn instruction for {token_account}")
            except Exception as e:
                logger.error(f"Error preparing burn instruction for {token_account}: {e}", exc_info=True)
                return

        close_account_instruction = close_account(
            CloseAccountParams(
                program_id=TOKEN_PROGRAM_ID,
                account=token_account_pubkey,
                dest=owner,
                owner=owner
            )
        )
        transaction.add(set_compute_unit_price(BurnValues.DEFAULT_COMPUTE_UNIT_PRICE))
        transaction.add(set_compute_unit_limit(BurnValues.DEFAULT_COMPUTE_UNIT_LIMIT))
        transaction.add(close_account_instruction)

        try:
            transaction.sign(agent.wallet)
            txn_sig = client.send_transaction(transaction, agent.wallet, opts=TxOpts(skip_preflight=True)).value
            logger.info(f"Transaction signature for {token_account}: {txn_sig}")
        except Exception as e:
            logger.error(f"Error sending transaction for {token_account}: {e}", exc_info=True)

    @staticmethod
    def process_multiple_accounts(agent: SolanaAgentKit, token_accounts: list):
        """
        Processes multiple token accounts by burning and closing each one.

        Parameters:
        agent (SolanaAgentKit): The agent instance containing wallet and RPC configuration.
        token_accounts (list): List of token account public keys as strings.
        """
        for token_account in token_accounts:
            try:
                logger.info(f"Processing token account: {token_account}")
                BurnManager.burn_and_close_account(agent, token_account)
            except Exception as e:
                logger.error(f"Error processing token account {token_account}: {e}", exc_info=True)
