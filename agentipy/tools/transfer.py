import logging

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.message import Message  # type: ignore
from solders.pubkey import Pubkey as PublicKey  # type: ignore
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction  # type: ignore
from spl.token.async_client import AsyncToken
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import get_associated_token_address, transfer_checked
from solders.null_signer import NullSigner
from agentipy.agent import SolanaAgentKit
from agentipy.wallet.privy_wallet_client import PrivyWalletClient
from agentipy.wallet.solana_wallet_client import SolanaWalletClient, SolanaTransaction
import base64

LAMPORTS_PER_SOL = 10**9

logger = logging.getLogger(__name__)


class TokenTransferManager:
    @staticmethod
    async def transfer(
        agent: SolanaAgentKit, to: str, amount: float, mint: str = None
    ) -> str:
        """
        Transfer SOL or SPL tokens to a recipient.
        """
        try:
            print(
                f"Transferring {amount} {'SPL' if mint else 'SOL'} to {to} from {agent.wallet_address}"
            )
            to_pubkey = PublicKey.from_string(to)
            from_pubkey = PublicKey.from_string(str(agent.wallet_address))

            blockhash_resp = await agent.connection.get_latest_blockhash()
            recent_blockhash = blockhash_resp.value.blockhash

            instructions = []

            if mint is None:
                instructions.append(
                    transfer(
                        TransferParams(
                            from_pubkey=from_pubkey,
                            to_pubkey=to_pubkey,
                            lamports=int(amount * LAMPORTS_PER_SOL),
                        )
                    )
                )
            else:
                mint_pubkey = PublicKey.from_string(mint)

                async with AsyncClient(agent.rpc_url) as client:
                    token = AsyncToken(client, mint_pubkey)

                    from_ata = await token.get_associated_token_address(from_pubkey)
                    to_ata = await token.get_associated_token_address(to_pubkey)

                    resp = await client.get_account_info(to_ata)
                    if resp.value is None:
                        from spl.token.instructions import (
                            create_associated_token_account,
                        )

                        ata_ix = create_associated_token_account(
                            from_pubkey, to_pubkey, mint_pubkey
                        )
                        instructions.append(ata_ix)

                    mint_info = await token.get_mint_info()
                    adjusted_amount = int(amount * (10**mint_info.decimals))

                    instructions.append(
                        transfer_checked(
                            source=from_ata,
                            dest=to_ata,
                            owner=from_pubkey,
                            amount=adjusted_amount,
                            decimals=mint_info.decimals,
                            mint=mint_pubkey,
                            program_id=TOKEN_PROGRAM_ID,
                        )
                    )

            # Detect Wallet Client Type
            if isinstance(agent.wallet_client, PrivyWalletClient):
                transaction = Transaction()
                for instruction in instructions:
                    transaction.add(instruction)
                transaction.recent_blockhash = recent_blockhash
                serialized_transaction = transaction.serialize(verify_signatures=False)
                transaction_base64 = base64.b64encode(serialized_transaction).decode(
                    "utf-8"
                )
                res = await agent.wallet_client.send_transaction(transaction_base64)
                tx_id = res.get("hash", "tx_id")
            elif isinstance(agent.wallet_client, SolanaWalletClient):
                solana_tx = SolanaTransaction(instructions=instructions)
                res = await agent.wallet_client.send_transaction(solana_tx)
                tx_id = res.get("hash", "tx_id")
            else:
                # Fallback for other wallet types
                raise ValueError(
                    f"Unsupported wallet client type: {type(agent.wallet_client).__name__}"
                )

            logging.info(f"Transaction Signature: {tx_id}")
            return str(tx_id)

        except Exception as e:
            raise RuntimeError(f"Transfer failed: {str(e)}")
