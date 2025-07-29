import base64

import aiohttp
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.message import MessageV0, to_bytes_versioned  # type: ignore
from solders.transaction import VersionedTransaction  # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import fix_asyncio_for_windows
from agentipy.wallet.privy_wallet_client import PrivyWalletClient
from agentipy.wallet.solana_wallet_client import SolanaWalletClient

fix_asyncio_for_windows()


class StakeManager:
    @staticmethod
    async def stake_with_jup(agent: SolanaAgentKit, amount: float) -> dict:
        """
        Stake SOL with Jup validator.

        Args:
            agent (SolanaAgentKit): The agent instance for Solana interaction.
            amount (float): The amount of SOL to stake.

        Returns:
            dict: Transaction metadata including signature, slot, and explorer URL.

        Raises:
            Exception: If the staking process fails.
        """
        try:
            url = f"https://worker.jup.ag/blinks/swap/So11111111111111111111111111111111111111112/jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v/{amount}"
            payload = {"account": str(agent.wallet_address)}

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as res:
                    if res.status != 200:
                        raise Exception(f"Failed to fetch transaction: {res.status}")
                    data = await res.json()

            latest_blockhash = await agent.connection.get_latest_blockhash()

            if isinstance(agent.wallet_client, PrivyWalletClient):
                res = await agent.wallet_client.send_transaction(data["transaction"])
                tx_id = res.get("hash", "tx_id")
                signature = tx_id

            elif isinstance(agent.wallet_client, SolanaWalletClient):
                transaction = VersionedTransaction.from_bytes(
                    base64.b64decode(data["transaction"])
                )
                signature = agent.wallet.sign_message(
                    to_bytes_versioned(transaction.message)
                )
                signed_transaction = VersionedTransaction.populate(
                    transaction.message, [signature]
                )
                tx_resp = await agent.connection.send_transaction(
                    signed_transaction,
                    opts=TxOpts(
                        preflight_commitment=Confirmed,
                        skip_preflight=False,
                        max_retries=3,
                    ),
                )
                tx_id = tx_resp.value
                signature = tx_id

            else:
                raise ValueError(
                    f"Unsupported wallet client type: {type(agent.wallet_client).__name__}"
                )

            if isinstance(signature, str):
                from solders.signature import Signature  # type: ignore
                signature = Signature.from_string(signature)

            await agent.connection.confirm_transaction(
                tx_sig=signature,
                commitment=Confirmed,
                last_valid_block_height=latest_blockhash.value.last_valid_block_height,
            )

            slot = confirmation_resp.context.slot
            explorer_url = f"https://solscan.io/tx/{tx_id}"

            return {
                "signature": str(signature),
                "tx_id": tx_id,
                "slot": slot,
                "explorer": explorer_url,
                "confirmed": confirmation_resp.value
            }

        except Exception as e:
            raise Exception(f"jupSOL staking failed: {str(e)}")
