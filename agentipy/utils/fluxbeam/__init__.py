from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey  # type: ignore
from spl.token.client import Token
from spl.token.constants import TOKEN_2022_PROGRAM_ID, TOKEN_PROGRAM_ID

from agentipy.agent import SolanaAgentKit


async def get_token_decimals(agent: SolanaAgentKit, mint: Pubkey) -> int:
    """
    Get the number of decimals for a given token mint address.

    Args:
        agent (SolanaAgentKit): The Solana agent instance.
        mint (Pubkey): The mint address of the token.

    Returns:
        int: The number of decimals for the token.

    Raises:
        Exception: If fetching mint info fails for both standard and Token 2022 program.
    """
    try:
        token_client = Token(agent.connection, mint, TOKEN_PROGRAM_ID, agent.wallet)
        mint_info = await token_client.get_mint_info()
        return mint_info.decimals
    except Exception:
        try:
            token_client = Token(agent.connection, mint, TOKEN_2022_PROGRAM_ID, agent.wallet.payer)
            mint_info = await token_client.get_mint_info()
            return mint_info.decimals
        except Exception as final_error:
            raise Exception(f"Failed to fetch mint info for token {mint}: {str(final_error)}")
