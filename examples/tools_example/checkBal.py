import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.get_balance import BalanceFetcher
from solders.pubkey import Pubkey
import base58

async def main():

    agent = SolanaAgentKit(
        private_key="",
        rpc_url="https://api.mainnet.solana.com"
    )

    try:
        sol_balance = await BalanceFetcher.get_balance(agent)
        print(f"SOL Balance: {sol_balance} SOL")
    except Exception as e:
        print(f"Failed to fetch SOL balance: {e}")

    
if __name__ == "__main__":
    asyncio.run(main())
