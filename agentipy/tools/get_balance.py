from typing import Optional

from solana.rpc.commitment import Confirmed
from solders.pubkey import Pubkey  # type: ignore
from spl.token.instructions import get_associated_token_address

from agentipy.agent import SolanaAgentKit
from agentipy.constants import LAMPORTS_PER_SOL


class BalanceFetcher:
    @staticmethod
    async def get_balance(
        agent: SolanaAgentKit, token_address: Optional[str] = None
    ) -> Optional[float]:
        """
        Get the balance of SOL or an SPL token for the agent's wallet.

        Args:
            agent: SolanaAgentKit instance.
            token_address: Optional SPL token mint address. If not provided, returns SOL balance.

        Returns:
            Balance as a float in UI units, or None if the account doesn't exist.

        Raises:
            Exception: If the balance check fails.
        """
        try:
            if not token_address:
                response = await agent.connection.get_balance(
                    agent.wallet_address, commitment=Confirmed
                )
                return response.value / LAMPORTS_PER_SOL

            token_account_pubkey = get_associated_token_address(
                owner=agent.wallet_address, mint=Pubkey.from_string(token_address)
            )

            response = await agent.connection.get_token_account_balance(
                token_account_pubkey, commitment=Confirmed
            )

            if response.value is None:
                return None

            return float(response.value.ui_amount)

        except Exception as error:
            raise Exception(
                f"Failed to get balance for {'SOL' if not token_address else 'SPL token'}: {str(error)}"
            ) from error
