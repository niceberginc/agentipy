import base64
import asyncio
import aiohttp
import platform

from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.message import to_bytes_versioned  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solders.transaction import VersionedTransaction  # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.constants import (DEFAULT_OPTIONS, JUP_API, LAMPORTS_PER_SOL,
                                TOKENS)
# from agentipy.helpers import fix_asyncio_for_windows #Removed because it is not needed anymore.

if platform.system() == "Windows": #Added the aiodns fix.
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) #Added the aiodns fix.

# fix_asyncio_for_windows() #Removed because it is not needed anymore.

class TradeManager:
    @staticmethod
    async def trade(
        agent: SolanaAgentKit,
        output_mint: Pubkey,
        input_amount: float,
        input_mint: Pubkey = TOKENS["USDC"],
        slippage_bps: int = DEFAULT_OPTIONS["SLIPPAGE_BPS"],
    ) -> str:
        """
        Swap tokens using Jupiter Exchange.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            output_mint (Pubkey): Target token mint address.
            input_amount (float): Amount to swap (in token decimals).
            input_mint (Pubkey): Source token mint address (default: USDC).
            slippage_bps (int): Slippage tolerance in basis points (default: 300 = 3%).

        Returns:
            str: Transaction signature.

        Raises:
            Exception: If the swap fails.
        """
        try:
            quote_url = (
                f"{JUP_API}/quote?"
                f"inputMint={input_mint}"
                f"&outputMint={output_mint}"
                f"&amount={int(input_amount * LAMPORTS_PER_SOL)}"
                f"&slippageBps={slippage_bps}"
                f"&onlyDirectRoutes=true"
                f"&maxAccounts=20"
            )

            async with aiohttp.ClientSession() as session:
                async with session.get(quote_url) as quote_response:
                    if quote_response.status != 200:
                        raise Exception(f"Failed to fetch quote: {quote_response.status}")
                    quote_data = await quote_response.json()

                async with session.post(
                    f"{JUP_API}/swap",
                    json={
                        "quoteResponse": quote_data,
                        "userPublicKey": str(agent.wallet_address),
                        "wrapAndUnwrapSol": True,
                        "dynamicComputeUnitLimit": True,
                        "prioritizationFeeLamports": "auto",
                    },
                ) as swap_response:
                    if swap_response.status != 200:
                        raise Exception(f"Failed to fetch swap transaction: {swap_response.status}")
                    swap_data = await swap_response.json()

            swap_transaction_buf = base64.b64decode(swap_data["swapTransaction"])
            transaction = VersionedTransaction.from_bytes(swap_transaction_buf)

            latest_blockhash = await agent.connection.get_latest_blockhash()

            signature = agent.wallet.sign_message(to_bytes_versioned(transaction.message))
            signed_transaction = VersionedTransaction.populate(transaction.message, [signature])

            tx_resp = await agent.connection.send_transaction(
                signed_transaction,
                opts=TxOpts(preflight_commitment=Confirmed, skip_preflight=False, max_retries=3),
            )
            tx_id = tx_resp.value

            await agent.connection.confirm_transaction(
                tx_id,
                commitment=Confirmed,
                last_valid_block_height=latest_blockhash.value.last_valid_block_height,
            )

            return str(signature)

        except Exception as e:
            raise Exception(f"Swap failed: {str(e)}")