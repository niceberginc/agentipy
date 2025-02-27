import base64

import aiohttp
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.message import to_bytes_versioned  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solders.transaction import VersionedTransaction  # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.constants import FLUXBEAM_BASE_URI, TOKENS
from agentipy.utils.fluxbeam import get_token_decimals


class FluxBeamManager:
    @staticmethod
    async def fluxbeam_create_pool(
        agent: SolanaAgentKit,
        token_a: Pubkey,
        token_a_amount: float,
        token_b: Pubkey,
        token_b_amount: float
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
        try:
            is_token_a_native_sol = token_a == TOKENS["SOL"]
            token_a_decimals = 9 if is_token_a_native_sol else await get_token_decimals(agent, token_a)

            scaled_amount_token_a = token_a_amount * (10 ** token_a_decimals)

            is_token_b_native_sol = token_b == TOKENS["SOL"]
            token_b_decimals = 9 if is_token_b_native_sol else await get_token_decimals(agent, token_b)

            scaled_amount_token_b = token_b_amount * (10 ** token_b_decimals)

            request_body = {
                "payer": str(agent.wallet_address),
                "token_a": str(token_a),
                "token_b": str(token_b),
                "token_a_amount": scaled_amount_token_a,
                "token_b_amount": scaled_amount_token_b
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{FLUXBEAM_BASE_URI}/token_pools",
                    json=request_body,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status != 200:
                        raise Exception(f"FluxBeam API request failed: {response.status}")

                    response_data = await response.json()

                    if "error" in response_data:
                        raise Exception(response_data["error"])

                    transaction_buf = base64.b64decode(response_data["transaction"])
                    transaction = VersionedTransaction.from_bytes(transaction_buf)

                    latest_blockhash = await agent.connection.get_latest_blockhash()

                    signature = agent.wallet.sign_message(to_bytes_versioned(transaction.message))
                    signed_transaction = VersionedTransaction.populate(transaction.message, [signature])

                    tx_resp = await agent.connection.send_transaction(
                        signed_transaction,
                        opts=TxOpts(preflight_commitment=Confirmed, skip_preflight=True, max_retries=3)
                    )
                    tx_id = tx_resp.value

                    await agent.connection.confirm_transaction(
                        tx_id,
                        commitment=Confirmed,
                        last_valid_block_height=latest_blockhash.value.last_valid_block_height
                    )

                    return str(signature)

        except Exception as e:
            raise Exception(f"Failed to create FluxBeam pool: {str(e)}")
