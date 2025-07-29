import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.stake_with_jup import StakeManager



async def main():
    agent = SolanaAgentKit(
        private_key="", 
        rpc_url="https://api.mainnet-beta.solana.com"
    )  

    amount = 0.01

    try:
        print(f" Staking {amount} SOL with jupSOL validator...")
        result = await StakeManager.stake_with_jup(agent, amount)

        print("\n Transaction Complete!")
        print(f" Signature: {result['signature']}")
        print(f" Slot: {result['slot']}")
        print(f" Confirmed: {result['confirmed']}")
        print(f" Explorer: {result['explorer']}")

    except Exception as e:
        print(f" Failed to stake SOL: {e}")

if __name__ == "__main__":
    asyncio.run(main())

