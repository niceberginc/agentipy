import base64
import aiohttp
from solana.rpc.commitment import Confirmed
from solders.message import to_bytes_versioned, MessageV0 
from solders.transaction import VersionedTransaction  

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import fix_asyncio_for_windows

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

            txn = VersionedTransaction.from_bytes(base64.b64decode(data["transaction"]))
            latest_blockhash = await agent.connection.get_latest_blockhash()

            signature = agent.wallet.sign_message(to_bytes_versioned(txn.message))
            signed_tx = VersionedTransaction.populate(txn.message, [signature])

            tx_resp = await agent.connection.send_transaction(signed_tx)

            tx_id = tx_resp.value

            confirmation_resp = await agent.connection.confirm_transaction(
                tx_id,
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
