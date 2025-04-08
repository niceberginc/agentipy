import logging
from typing import Any, Dict

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.compute_budget import set_compute_unit_price  # type: ignore
from solders.keypair import Keypair  # type: ignore
from solders.message import Message, to_bytes_versioned  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solders.system_program import CreateAccountParams, create_account
from solders.transaction import Transaction  # type: ignore
from spl.token._layouts import MINT_LAYOUT
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import (InitializeMintParams, MintToParams,
                                    create_associated_token_account,
                                    get_associated_token_address,
                                    initialize_mint, mint_to)

from agentipy.agent import SolanaAgentKit

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

            sender = agent.wallet
            client = agent.connection
            sender_ata = get_associated_token_address(sender.pubkey(), new_mint.pubkey())

            blockhash = await client.get_latest_blockhash()

            lamports = (await client.get_minimum_balance_for_rent_exemption(MINT_LAYOUT.sizeof())).value

            create_account_ix = create_account(CreateAccountParams(
                from_pubkey=sender.pubkey(),
                to_pubkey=new_mint.pubkey(),
                owner=TOKEN_PROGRAM_ID,
                lamports=lamports,
                space=MINT_LAYOUT.sizeof(),
            ))

            initialize_mint_ix = initialize_mint(InitializeMintParams(
                decimals=decimals,
                freeze_authority=sender.pubkey(),
                mint=new_mint.pubkey(),
                mint_authority=sender.pubkey(),
                program_id=TOKEN_PROGRAM_ID,
            ))


            create_associated_token_account_ix = create_associated_token_account(sender.pubkey(), sender.pubkey(), new_mint.pubkey())

            amount_to_transfer = 1000000000 * 10 ** 8


            mint_to_ix = mint_to(MintToParams(
                amount=amount_to_transfer,
                dest=sender_ata,
                mint=new_mint.pubkey(),
                mint_authority=sender.pubkey(),
                program_id=TOKEN_PROGRAM_ID,
            ))

            message = Message([
                create_account_ix,
                initialize_mint_ix,
                create_associated_token_account_ix,
                mint_to_ix,
            ], sender.pubkey())


            blockhash_response = await agent.connection.get_latest_blockhash()
            recent_blockhash = blockhash_response.value.blockhash

            transaction = Transaction([sender, new_mint], message, recent_blockhash=recent_blockhash)

            tx_resp = await agent.connection.send_transaction(transaction, opts=TxOpts(preflight_commitment=Confirmed))

            tx_id = tx_resp.value

            await agent.connection.confirm_transaction(
                tx_id,
                commitment=Confirmed,
                last_valid_block_height=blockhash.value.last_valid_block_height,
            )

            logger.info(f"https://explorer.solana.com/tx/{tx_resp}")

            await client.close()

            logger.info(f"Transaction Signature: {tx_resp}")

            return {
                "mint": str(new_mint.pubkey()),
                "signature": tx_resp,
            }

        except Exception as e:
            logger.error(f"Token deployment failed: {str(e)}")
            raise Exception(f"Token deployment failed: {str(e)}")
