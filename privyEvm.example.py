import asyncio

from agentipy import EvmAgentKit
import agentipy
from agentipy import SolanaAgentKit
from agentipy.agent.evm import WalletType
from agentipy.tools.get_balance import BalanceFetcher
from agentipy.tools.trade import TradeManager
from agentipy.tools.transfer import TokenTransferManager


from agentipy.utils.evm.general.networks import BaseRPC
from agentipy.utils.evm.tokens.base import USDC_BASE, WETH_BASE  # type: ignore

print(agentipy.__name__)

agent = EvmAgentKit(
    network=BaseRPC,
    wallet_type=WalletType.PRIVY,
    privy_app_secret="",
    privy_app_id="",
    privy_wallet_id="",
)

addressToTransfer = ""


async def transfer():
    transfer = await TokenTransferManager.transfer(agent, addressToTransfer, 0.0001)


async def swap():
    trade = await agent.trade_on_uniswap(
        input_token_address=WETH_BASE.address,
        output_token_address=USDC_BASE.address,
        amount_in_raw="5000000000000",
        input_token_decimals=WETH_BASE.decimals,
        output_token_decimals=USDC_BASE.decimals,
        slippage=0.5,
    )


async def main():
    await transfer()
    # await swap()


asyncio.run(main())
