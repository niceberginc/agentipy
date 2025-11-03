import os
import asyncio
from dotenv import load_dotenv
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_g402 import G402DataFetcher
from agentipy.tools.get_balance import BalanceFetcher

load_dotenv()

async def main():
    private_key_b58 = os.getenv("CLIENT_WALLET_PRIVATE_KEY_BASE58")
    if not private_key_b58:
        raise SystemExit("Error: Set CLIENT_WALLET_PRIVATE_KEY_BASE58 in your .env file")

    premium_data_url = "http://127.0.0.1:8000/premium-data"

    agent = SolanaAgentKit(
        private_key=private_key_b58,
        rpc_url="https://api.devnet.solana.com"
    )

    print("Solana Agent Initialized.")
    print(f"Pubkey: {agent.wallet_address}")

    try:
        initial_balance = await BalanceFetcher.get_balance(agent)
        print(f"Balance before payment: {initial_balance} SOL")
    except Exception as e:
        print(f"Could not fetch initial balance: {e}")

    try:
        premium_data = await G402DataFetcher.fetch_premium_data(
            agent=agent,
            url=premium_data_url
        )

        print("\nAgent can now proceed with the premium data:")
        print(premium_data.get("data"))

        try:
            final_balance = await BalanceFetcher.get_balance(agent)
            print(f"Balance after payment: {final_balance} SOL")
        except Exception as e:
            print(f"Could not fetch final balance: {e}")

    except Exception as e:
        print(f"\nAn error occurred during the agent's operation: {e}")

if __name__ == "__main__":
    asyncio.run(main())