# Solana Agent Kit

A powerful toolkit for interacting with the Solana blockchain, providing easy-to-use functions for token operations, trading, and more. Now integrated with LangChain for enhanced functionality.

## Features

- 🪙 Token Operations

  - Transfer SOL and SPL tokens
  - Check token balances
  - Stake SOL
  - Deploy new tokens
  - Request faucet funds
  - Burn and close token accounts
  - Batch burn and close token accounts

- 💱 Trading

  - Integrated Jupiter Exchange support
  - Token swaps with customizable slippage
  - Direct routing options
  - Buy and sell tokens with Raydium liquidity

- 🏦 Yield Farming

  - Lend idle assets to earn interest with Lulo

- 🔗 LangChain Integration

  - Utilize LangChain tools for enhanced blockchain interactions
  - Access a suite of tools for balance checks, transfers, token deployments, and more

- 📈 Performance Tracking

  - Fetch current transactions per second (TPS) on the Solana network

- 📊 Token Data

  - Get token data by ticker
  - Get token data by address

- 🚀 Pump & Fun Tokens

  - Launch Pump & Fun tokens with customizable options

- 🏦 Meteora DLMM Pools

  - Create Meteora DLMM pools with various configurations

## Installation

```bash
pip install agentipy
```

## Quick Start

```python
from agentipy import SolanaAgentKit, create_solana_tools

# Initialize with private key and optional RPC URL
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)

# Create LangChain tools
tools = create_solana_tools(agent)
```

## Usage Examples

### Fetch price of a token

```python
from agentipy import SolanaAgentKit

async def main():
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)

    # Get balance
    balance =  await agent.fetch_price("FKMKctiJnbZKL16pCmR7ig6bvjcMJffuUMjB97YD7LJs")
    print(f"Price: {balance} SOL")

# Run the async function
import asyncio
asyncio.run(main())

```

### Swap Tokens

```python
from agentipy import SolanaAgentKit

from solders.pubkey import Pubkey

async def main():
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)

signature = await agent.trade(
    output_mint=Pubkey.from_string("target-token-mint"),
    input_amount=100,  # amount
    input_mint=Pubkey.from_string("source-token-mint"),
    slippage_bps=300  # 3% slippage
)

import asyncio
asyncio.run(main())
```

### Lend Tokens

```python
from agentipy import SolanaAgentKit

from solders.pubkey import Pubkey

async def main():
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)
signature = await agent.lend_assets(
    amount=100  # amount
)

import asyncio
asyncio.run(main())
```

### Stake SOL

```python
from agentipy import SolanaAgentKit

from solders.pubkey import Pubkey

async def main():
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)

signature = await agent.stake(
    amount=1  # amount in SOL
)

import asyncio
asyncio.run(main())
```

### Request Faucet Funds

```python
from agentipy import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    response = await agent.request_faucet_funds()
    print(response)

import asyncio
asyncio.run(main())
```

### Fetch Current TPS

```python
from agentipy import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    tps = await agent.get_tps()
    print(f"Current TPS: {tps}")

import asyncio
asyncio.run(main())
```

### Get Token Data by Ticker

```python
from agentipy import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    token_data = await agent.get_token_data_by_ticker("SOL")
    print(token_data)

import asyncio
asyncio.run(main())
```

### Get Token Data by Address

```python
from agentipy import SolanaAgentKit
from solders.pubkey import Pubkey

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    token_data = await agent.get_token_data_by_address("your-token-mint-address")
    print(token_data)

import asyncio
asyncio.run(main())
```

### Launch Pump Fun Token

```python
from agentipy import SolanaAgentKit
from agentipy.types import PumpfunTokenOptions

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    options = PumpfunTokenOptions(
        # Add your options here
    )

    response = await agent.launch_pump_fun_token(
        token_name="MyToken",
        token_ticker="MTK",
        description="This is a fun token",
        image_url="https://example.com/image.png",
        options=options
    )
    print(response)
```

### Create Meteora DLMM Pool

```python
from agentipy import SolanaAgentKit
from solders.pubkey import Pubkey
from agentipy.utils.meteora_dlmm.types import ActivationType

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    response = await agent.create_meteora_dlmm_pool(
        bin_step=1,
        token_a_mint=Pubkey.from_string("token-a-mint"),
        token_b_mint=Pubkey.from_string("token-b-mint"),
        initial_price=1.0,
        price_rounding_up=True,
        fee_bps=30,
        activation_type=ActivationType.Timestamp,
        has_alpha_vault=True,
        activation_point=None
    )
    print(response)

import asyncio
asyncio.run(main())
```

### Buy Tokens with Raydium

```python
from agentipy import SolanaAgentKit
from solders.pubkey import Pubkey

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    confirmed = await agent.buy_with_raydium(
        pair_address=Pubkey.from_string("target-pair-address"),  # The pair you want to buy from
        sol_in=1,  # Amount of SOL or input token to spend
        slippage=300  # Maximum slippage in basis points (3% here)
    )
    print(f"Transaction confirmed: {confirmed}")

import asyncio
asyncio.run(main())
```

### Sell Tokens with Raydium

```python
from agentipy import SolanaAgentKit
from solders.pubkey import Pubkey

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    confirmed = await agent.sell_with_raydium(
        input_mint=Pubkey.from_string("source-token-mint"),  # The token you want to sell
        percentage=100,
        slippage_bps=250  # Maximum slippage in basis points (2.5% here)
    )
    print(f"Transaction confirmed: {confirmed}")

import asyncio
asyncio.run(main())
```

### Burn and Close Token Account

```python
from agentipy import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    response = await agent.burn_and_close_accounts("token-account-address")
    print("Account burned and closed:", response)

import asyncio
asyncio.run(main())
```

### Batch burn and Close Token Account

```python
from agentipy import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        "your-wallet-private-key-as-base58",
        "https://api.mainnet-beta.solana.com",
        "your-openai-api-key"
    )

    token_accounts = ["token-account-address-1", "token-account-address-2"]
    responses = await agent.multiple_burn_and_close_accounts(token_accounts)
    print("Accounts burned and closed:", responses)

import asyncio
asyncio.run(main())
```

## API Reference

### Core Functions

#### `transfer(agent, to, amount, mint?)`

Transfer SOL or SPL tokens to a recipient.

#### `trade(agent, output_mint, input_amount, input_mint?, slippage_bps?)`

Swap tokens using Jupiter Exchange integration.

#### `get_balance(agent, token_address)`

Check SOL or token balance for the agent's wallet.

#### `lend_asset(agent, asset_mint, amount)`

Lend idle assets to earn interest with Lulo.

#### `stake(agent, amount)`

Stake SOL with Jupiter to earn rewards.

#### `request_faucet_funds(agent)`

Request faucet funds for testing purposes.

#### `deploy_token(agent, decimals)`

Deploy a new token with specified decimals.

#### `fetch_price(agent, token_id)`

Fetch the price of a token.

#### `get_tps(agent)`

Fetch the current transactions per second (TPS) on the Solana network.

#### `get_token_data_by_ticker(agent, ticker)`

Get token data by ticker.

#### `get_token_data_by_address(agent, mint)`

Get token data by address.

#### `launch_pump_fun_token(agent, token_name, token_ticker, description, image_url, options)`

Launch a Pump & Fun token with customizable options.

#### `create_meteora_dlmm_pool(agent, bin_step, token_a_mint, token_b_mint, initial_price, price_rounding_up, fee_bps, activation_type, has_alpha_vault, activation_point)`

Create a Meteora DLMM pool with various configurations.

#### `buy_with_raydium(agent, pair_address, sol_in, slippage)`

Buy tokens from Raydium liquidity pools.

#### `sell_with_raydium(agent, pair_address, percentage, slippage)`

Sell tokens using Raydium liquidity pools.

#### `burn_and_close_accounts(agent, token_account)`

Burns and closes token account.

#### `multiple_burn_and_close_accounts(agent, token_accounts)`

Burns and closes multiple token accounts.

## Dependencies

The toolkit relies on several key Solana and Metaplex libraries:

- solana-py
- spl-token-py

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

ISC License

## Security

This toolkit handles private keys and transactions. Always ensure you're using it in a secure environment and never share your private keys.
