import asyncio
import agentipy
from agentipy import SolanaAgentKit
from agentipy.tools.get_balance import BalanceFetcher
from agentipy.tools.trade import TradeManager
from agentipy.tools.transfer import TokenTransferManager
from solders.pubkey import Pubkey  # type: ignore

print(agentipy.__name__)

""" agent = SolanaAgentKit(
    private_key="",
    rpc_url="https://api.mainnet-beta.solana.com",
) """

agent = SolanaAgentKit(
    use_privy_wallet=True,
    privy_app_secret="",
    privy_app_id="",
    generate_wallet=False,
    privy_wallet_id="",
)

addressToTransfer = ""


async def getBalance():
    bal = await BalanceFetcher.get_balance(agent)
    print("balance is: ", bal)


async def transfer():
    transfer = await TokenTransferManager.transfer(agent, addressToTransfer, 0.0001)
    print("wallet", transfer)


async def swap():
    USDC_MINT = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
    SOL_MINT = Pubkey.from_string("So11111111111111111111111111111111111111112")

    SWAP_AMOUNT_SOL = 0.0001
    transaction_signature = await TradeManager.trade(
        agent=agent,
        output_mint=USDC_MINT,
        input_amount=SWAP_AMOUNT_SOL,
        input_mint=SOL_MINT,
    )

    print(transaction_signature)


async def stake():
    transaction_signature = await agent.stake(100)
    print(transaction_signature)


async def main():
    await getBalance()
    # await transfer()
    # await swap()
    # await stake()


asyncio.run(main())
