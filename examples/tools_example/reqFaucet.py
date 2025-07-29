import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.request_faucet_funds import FaucetManager
from solders.keypair import Keypair
import base58

async def main():
    agent = SolanaAgentKit(
        private_key="",
        rpc_url="https://api.mainnet.solana.com"
    )

    try:
        tx_signature = await FaucetManager.request_faucet_funds(agent)
        print(f"Faucet airdrop completed. Transaction Signature: {tx_signature}")
    except Exception as e:
        print(f"Faucet airdrop failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
