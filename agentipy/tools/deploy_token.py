import base64
import logging
from typing import Any, Dict
from solders.signature import Signature  # type: ignore
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.compute_budget import set_compute_unit_price  # type: ignore
from solders.keypair import Keypair  # type: ignore
from solders.pubkey import Pubkey as PublicKey  # type: ignore
from solders.message import Message, to_bytes_versioned  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solders.system_program import CreateAccountParams, create_account
from solders.transaction import Transaction  # type: ignore
from spl.token._layouts import MINT_LAYOUT
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import (
    InitializeMintParams,
    MintToParams,
    create_associated_token_account,
    get_associated_token_address,
    initialize_mint,
    mint_to,
)

from agentipy.agent import SolanaAgentKit
from agentipy.wallet.privy_wallet_client import PrivyWalletClient
from agentipy.wallet.solana_wallet_client import SolanaTransaction, SolanaWalletClient

logger = logging.getLogger(__name__)


class TokenDeploymentManager:
    @staticmethod
    async def deploy_token(agent: SolanaAgentKit, decimals: int = 9) -> Dict[str, Any]:
        """
        Deploy a new SPL token.

        Args:
            agent: SolanaAgentKit instance with wallet and connection.
            decimals: Number of decimals for the token (default: 9).

        Returns:
            A dictionary containing the token mint address.
        """
        try:
            new_mint = Keypair()
            logger.info(f"Generated mint address: {new_mint.pubkey()}")

            sender_pubkey = PublicKey.from_string(str(agent.wallet_address))
            sender_ata = get_associated_token_address(sender_pubkey, new_mint.pubkey())

            blockhash_response = await agent.connection.get_latest_blockhash()
            recent_blockhash = blockhash_response.value.blockhash

            lamports = (
                await agent.connection.get_minimum_balance_for_rent_exemption(
                    MINT_LAYOUT.sizeof()
                )
            ).value

            create_account_ix = create_account(
                CreateAccountParams(
                    from_pubkey=sender_pubkey,
                    to_pubkey=new_mint.pubkey(),
                    owner=TOKEN_PROGRAM_ID,
                    lamports=lamports,
                    space=MINT_LAYOUT.sizeof(),
                )
            )

            initialize_mint_ix = initialize_mint(
                InitializeMintParams(
                    decimals=decimals,
                    freeze_authority=sender_pubkey,
                    mint=new_mint.pubkey(),
                    mint_authority=sender_pubkey,
                    program_id=TOKEN_PROGRAM_ID,
                )
            )

            create_associated_token_account_ix = create_associated_token_account(
                sender_pubkey, sender_pubkey, new_mint.pubkey()
            )

            amount_to_transfer = 1000000000 * 10**8

            mint_to_ix = mint_to(
                MintToParams(
                    amount=amount_to_transfer,
                    dest=sender_ata,
                    mint=new_mint.pubkey(),
                    mint_authority=sender_pubkey,
                    program_id=TOKEN_PROGRAM_ID,
                )
            )

            instructions = [
                create_account_ix,
                initialize_mint_ix,
                create_associated_token_account_ix,
                mint_to_ix,
            ]

            # Detect Wallet Client Type
            if isinstance(agent.wallet_client, PrivyWalletClient):
                transaction = Transaction()
                for instruction in instructions:
                    transaction.add(instruction)
                transaction.recent_blockhash = recent_blockhash
                # Add new_mint as signer to the transaction
                transaction.sign_partial(new_mint)
                serialized_transaction = transaction.serialize(verify_signatures=False)
                transaction_base64 = base64.b64encode(serialized_transaction).decode(
                    "utf-8"
                )
                res = await agent.wallet_client.send_transaction(transaction_base64)
                tx_id = res.get("hash", "tx_id")
            elif isinstance(agent.wallet_client, SolanaWalletClient):
                solana_tx = SolanaTransaction(
                    instructions=instructions, signers=[new_mint]
                )
                res = await agent.wallet_client.send_transaction(solana_tx)
                tx_id = res.get("hash", "tx_id")
            else:
                # Fallback for other wallet types
                raise ValueError(
                    f"Unsupported wallet client type: {type(agent.wallet_client).__name__}"
                )

            logger.info(f"Transaction Signature: {tx_id}")
            await agent.connection.confirm_transaction(
                tx_id,
                commitment=Confirmed,
                last_valid_block_height=blockhash_response.value.last_valid_block_height,
            )

            return {
                "mint": str(new_mint.pubkey()),
                "signature": tx_id,
            }

        except Exception as e:
            logger.error(f"Token deployment failed: {str(e)}")
            raise Exception(f"Token deployment failed: {str(e)}")
