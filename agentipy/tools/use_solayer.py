import base64
import json

import aiohttp
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.message import to_bytes_versioned  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solders.transaction import VersionedTransaction  # type: ignore

from agentipy.agent import SolanaAgentKit


class SolayerManager:
    BASE_URL = "https://app.solayer.org/api/action/restake/ssol"

    @staticmethod
    async def stake_with_solayer(agent: SolanaAgentKit, amount: float) -> str:
        """
        Stake SOL with Solayer.

        Args:
            agent (SolanaAgentKit): SolanaAgentKit instance.
            amount (float): Amount of SOL to stake.

        Returns:
            str: Transaction signature.
        """
        try:
            url = f"{SolayerManager.BASE_URL}?amount={amount}"
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({"account": str(agent.wallet_address)})

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    if response.status != 200:
                        error_data = await response.json()
                        raise Exception(error_data.get("message", "Staking request failed"))
                    data = await response.json()

            transaction_bytes = base64.b64decode(data["transaction"])
            txn = VersionedTransaction.from_bytes(transaction_bytes)

            latest_blockhash = await agent.connection.get_latest_blockhash()

            signature = agent.wallet.sign_message(to_bytes_versioned(txn.message))
            signed_tx = VersionedTransaction.populate(txn.message, [signature])

            tx_resp = await agent.connection.send_transaction(
                signed_tx,
                opts=TxOpts(preflight_commitment=Confirmed, max_retries=3)
            )
            tx_id = tx_resp.value

            await agent.connection.confirm_transaction(
                tx_id,
                commitment=Confirmed,
                last_valid_block_height=latest_blockhash.value.last_valid_block_height,
            )

            return str(signature)

        except Exception as e:
            raise Exception(f"Solayer sSOL staking failed: {str(e)}")
