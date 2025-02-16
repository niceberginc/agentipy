class Network:
    def __init__(
            self,
            name: str,
            rpc: list,
            chain_id: int,
            eip1559_support: bool,
            token: str,
            explorer: str,
            decimals: int = 18
    ):
        self.name = name
        self.rpc = rpc
        self.chain_id = chain_id
        self.eip1559_support = eip1559_support
        self.token = token
        self.explorer = explorer
        self.decimals = decimals

    def __repr__(self):
        return f'{self.name}'
    

EthereumRPC = Network(
    name='Ethereum',
    rpc='https://rpc.ankr.com/eth',
    chain_id=1,
    eip1559_support=True,
    token='ETH',
    explorer='https://etherscan.io/'
)

BaseRPC = Network(
    name='Base',
    rpc='https://mainnet.base.org',
    chain_id=8453,
    eip1559_support=False,
    token='ETH',
    explorer='https://basescan.org/'
)

ArbitrumRPC = Network(
    name="Arbitrum",
    rpc='https://rpc.ankr.com/arbitrum/',
    chain_id=42161,
    eip1559_support=True,
    token="ETH",
    explorer='https://arbiscan.io/'
)
