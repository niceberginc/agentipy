from agentipy.utils.evm.general.networks import BaseRPC


class Token:
    def __init__(
            self,
            chainId: int,
            address: list,
            decimals: int = 18
    ):
        self.chainId = chainId
        self.address = address
        self.decimals = decimals

    def __repr__(self):
        return f'{self.name}'

WETH_BASE = Token(
    chainId=BaseRPC,
    address="0x4200000000000000000000000000000000000006",
    decimals=18
)

USDC_BASE = Token(
    chainId=BaseRPC,
    address="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    decimals=6
)