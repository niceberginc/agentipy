# AgentiPy: Your AI Agent Toolkit for Blockchain Applications

AgentiPy is a Python toolkit designed to empower AI agents to interact seamlessly with blockchain applications, focusing on Solana and Base. It simplifies the development of decentralized applications (dApps) by providing tools for token management, NFT handling, and more. With a focus on ease of use and powerful functionality, AgentiPy allows developers to create robust and sophisticated blockchain-based solutions, leveraging AI-driven workflows.

[<img src="https://img.shields.io/github.com/niceberginc/agentipy/agentipy?style=social" alt="GitHub Stars">](hhttps://github.com/niceberginc/agentipy/agentipy)
[<img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">](https://github.com/niceberginc/agentipy/agentipy/blob/main/LICENSE)

## 🚀 Introduction

AgentiPy bridges the gap between AI agents and blockchain applications. It provides a streamlined development experience for building decentralized applications (dApps) that leverage the power of AI on Solana and Base. From automated trading to complex DeFi interactions, AgentiPy equips developers with the tools needed to build intelligent on-chain solutions.

## ✨ Key Features

*   **Broad Protocol Support:** Supports a wide range of protocols on Solana and Base (See Detailed Protocol Table Below).
*   **Asynchronous Operations:** Utilizes asynchronous programming for efficient blockchain interactions.
*   **Easy Integration:** Designed for seamless integration into existing AI agent frameworks and dApp projects.
*   **Comprehensive Toolset:** Provides tools for token trading, NFT management, DeFi interactions, and more.
*   **Extensible Design:** Allows developers to create custom protocols and actions.
*   **Coingecko Integration**: Enhanced with new tooling to explore trending tokens, prices, and new pools
*   **Streamlined Development:** Provides essential utility functions such as price fetching, balance checks, and transaction confirmation.

## 📦 Installation and Setup

Before you begin, ensure you have the following prerequisites:

*   **Python 3.8+:** Required for running the toolkit.
*   **Solana CLI:** For Solana-specific actions (e.g., wallet creation).
*   **Langchain:** For AI integration (`pip install langchain`).
*   **Wallet with Private Keys:**  Crucial for signing and sending transactions.  **Securely manage your private keys!**
*   **API Keys (Optional):** For accessing various blockchain networks or external data sources (e.g., CoinGecko, QuickNode).

Follow these steps to install and set up AgentiPy:

1.  **Create a Virtual Environment (Recommended):**  Isolate your project dependencies.
    ```bash
    python -m venv venv
    ```
2.  **Activate the Virtual Environment:**
    *   **Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
3.  **Install AgentiPy:**
    ```bash
    pip install agentipy
    ```
4.  **Verify Installation:**
    ```python
    import agentipy
    print(agentipy.__version__)  # Example output: 2.0.2
    ```

## 🛠️ Supported Protocols and Tools

AgentiPy supports a diverse set of protocols, each with specific actions. This table provides a quick reference:

| Protocol       | Blockchain | Actions                                                        | GitHub Tool Link                                                                            |
| :------------- | :--------- | :------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| Jupiter        | Solana     | Token swaps, direct routing, stake SOL                        | [Jupiter Swap Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/stake_with_jup.py) |
| PumpFun        | Solana     | Buy/sell tokens, launch tokens, retrieve/calculate pump curve states | [PumpFun Buy Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_pumpfun.py) |
| Raydium        | Solana     | Buy/sell tokens, provide liquidity                             | [Raydium Trade Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_raydium.py) |
| Metaplex       | Solana     | NFT minting, collection deployment, metadata/royalty management| [Metaplex Mint Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_metaplex.py) |
| DexScreener    | Solana     | Get token data by ticker/address                               | [DexScreener Data Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/get_token_data.py) |
| Helius         | Solana     | Fetch balances, NFT mint lists, events, webhooks             | [Helius Balance Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_helius.py) |
| MoonShot       | Solana     | Buy/sell with collateral, slippage options                    | [MoonShot Trade Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_moonshot.py) |
| SNS            | Solana     | Get token data by ticker/address                               | [SNS Data Tool](hhttps://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_sns.py) |
| Cybers         | Solana     | Authenticate wallet, create coin                             | [Cybers Auth Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_cybers.py) |
| Adrena         | Solana     | Open/close perpetual trades (long/short)                     | [Adrena Trade Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_adrena.py) |
| Drift          | Solana     | Manage user accounts, deposit/withdraw, perp trades, account info  | [Drift Account Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_drift.py) |
| Flash          | Solana     | Open/close trades                                               | [Flash Trade Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_flash.py) |
| Jito           | Solana     | Manage tip accounts, bundle transactions                      | [Jito Tip Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_jito.py) |
| Lulo           | Solana     | Lend assets to earn interest                                  | [Lulo Lend Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_lulo.py) |
| RugCheck       | Solana     | Fetch detailed/summary token reports                           | [RugCheck Report Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_rugcheck.py) |
| All Domains    | Solana     | Resolve domains, get owned domains                             | [All Domains Resolve Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_alldomains.py) |
| Orca           | Solana     | Manage liquidity pools, positions                              | [Orca Position Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_orca.py) |
| Backpack       | Solana     | Manage account balances, settings, borrowing                    | [Backpack Balance Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_backpack.py) |
| OpenBook       | Solana     | Create markets                                                   | [OpenBook Market Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_openpook.py) |
| Light Protocol | Solana     | Send compressed airdrops                                        | [Light Airdrop Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_lightprotocol.py) |
| Pyth Network   | Solana     | Fetch token prices                                              | [Pyth Price Fetch Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_pyth.py) |
| Manifest       | Solana     | Create markets, place/cancel orders                            | [Manifest Order Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_manifest.py) |
| Stork          | Solana     | Get real-time token price feed                                 | [Stork Price Feed Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_stork.py) |
| Gibwork        | Solana     | Create tasks with token rewards                                  | [Gibwork Task Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_gibwork.py) |
| Meteora        | Solana     | Create DLMM pools with configurations                           | [Meteora Pool Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/create_meteora_dlmm_pool.py) |
|StakeWithJup    | Solana     | Stakes JUP to earn JUP tokens                 | [Stake With Jup tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/stake_with_jup.py) |
|ThreeLand    | Solana     | ThreeLand NFT mint and deploy        | [ThreeLand NFT mint tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_3land.py) |




## 🚀 Quick Start Example

This example demonstrates transferring SOL on Solana.  **Replace the placeholder values with your actual wallet details.**

```python
from agentipy.solana import SolanaClient
```
### Replace with your private key (DO NOT HARDCODE IN PRODUCTION - use environment variables!)
```python
solana = SolanaClient(private_key="your_private_key_here")
```
# Get your wallet's SOL balance
```python
balance = solana.get_balance("your_wallet_address")
print(f"Balance: {balance} SOL")
```

# Transfer 1 SOL to a recipient
```python
solana.transfer_sol(to_address="recipient_wallet_address", amount=1.0)
print("Transfer successful!")
```

Important Security Note: Never hardcode your private key directly into your code. Use environment variables or secure key management systems in a production environment.


## Transfer SOL/SPL: Easily send tokens.

```python 

from agentipy.tools.transfer import TokenTransferManager
import asyncio
from agentipy.agent import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        private_key="",  # Replace with your private key
        rpc_url="https://api.devnet.solana.com" #example URL
    )

    try:
        transfer_signature = await TokenTransferManager.transfer(
        agent=agent, 
        to="C9K1BwJgCb35n8r1wW5xJpDq533mY6W845sK68S7yJGN", 
        amount=0.0001)
        print(f"Transfer successful, see transaction {transfer_signature}")
    except RuntimeError as e:
        print(f"Something didn't go right: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Jupiter Trade: Powerful token swapping.
```python
from agentipy.tools.trade import TradeManager
from solders.pubkey import Pubkey
import asyncio
from agentipy.agent import SolanaAgentKit

async def main():
    agent = SolanaAgentKit(
        private_key="",  # Replace with your private key
        rpc_url="https://api.devnet.solana.com" #example URL
    )
    try:
        usdc_mint = Pubkey.from_string("Gh9ZwEmdLJ8DscKzPWuJZ9REHzCwkgQMTrnCHy3PWTWp") #devnet USDC
        signature = await TradeManager.trade(
            agent=agent,
            output_mint=usdc_mint,
            input_amount=0.001,
            input_mint = Pubkey.from_string("So11111111111111111111111111111111111111112"), #solana
            slippage_bps=1000
        )
        print(f"Trade signature: {signature}")
    except RuntimeError as e:
        print(f"Something didn't go right: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Get Token Data: Useful for data analysis.
```python
from agentipy.tools.get_token_data import TokenDataManager
from solders.pubkey import Pubkey

usdc_mint = Pubkey.from_string("Gh9ZwEmdLJ8DscKzPWuJZ9REHzCwkgQMTrnCHy3PWTWp")

token_data = TokenDataManager.get_token_data_by_address(usdc_mint)

print(token_data) #Token(mint=' EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', symbol='USDC', name='USD Coin')
```

## Fetch Token Prices: To keep up with trends.
```python
import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.fetch_price import TokenPriceFetcher
async def main():
    agent = SolanaAgentKit(
        private_key="",  # Replace with your private key
        rpc_url="https://api.devnet.solana.com" #example URL
    )
    price = await TokenPriceFetcher.fetch_price("Gh9ZwEmdLJ8DscKzPWuJZ9REHzCwkgQMTrnCHy3PWTWp")
    print(price) #Prints the price of the ticker that you specify
if __name__ == "__main__":
    asyncio.run(main())
```

## Coingecko API: to easily fetch any token prices using its integration.
```python
import asyncio
import aiohttp
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_coingecko import CoingeckoManager

async def coingecko_example():
    #Replace these with your actual values and keys
    PRIVATE_KEY = ""  
    RPC_URL = "https://api.mainnet-beta.solana.com"
    COINGECKO_API_KEY = "your_valid_pro_api_key_here"  
    COINGECKO_DEMO_API_KEY = "" 
   

    agent = SolanaAgentKit(
        private_key=PRIVATE_KEY,
        rpc_url=RPC_URL,
        coingecko_api_key=COINGECKO_API_KEY,
        coingecko_demo_api_key=COINGECKO_DEMO_API_KEY
    )

    token_address = "So11111111111111111111111111111111111111112"
    token_address_list = [token_address]

    try:
        trending_tokens_data = await CoingeckoManager.get_trending_tokens(agent)
        print("\nTrending Tokens Data:")
        print(trending_tokens_data)
    except Exception as e:
        print(f"Error with trending tokens: {e}")

    try:
        token_price_data = await CoingeckoManager.get_token_price_data(agent, token_address_list)
        print("\nToken Price Data:")
        print(token_price_data)
    except Exception as e:
        print(f"Error with token price data: {e}")

    try:
        trending_pools_data = await CoingeckoManager.get_trending_pools(agent)
        print("\nTrending Pools Data:")
        print(trending_pools_data)
    except Exception as e:
        print(f"Error with trending pools: {e}")

    try:
        top_gainers_data = await CoingeckoManager.get_top_gainers(agent)
        print("\nTop Gainers Data:")
        print(top_gainers_data)
    except Exception as e:
        print(f"Error with top gainers: {e}")

    try:
        token_info_data = await CoingeckoManager.get_token_info(agent, token_address)
        print("\nToken Info Data:")
        print(token_info_data)
    except Exception as e:
        print(f"Error with token info: {e}")

    try:
        latest_pools_data = await CoingeckoManager.get_latest_pools(agent)
        print("\nLatest Pools Data:")
        print(latest_pools_data)
    except Exception as e:
        print(f"Error with latest pools: {e}")

if __name__ == "__main__":
    asyncio.run(coingecko_example())
```

## All Domains: Get any domain for user.
```python
import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_alldomains import AllDomainsManager

async def main():
    agent = SolanaAgentKit(
        private_key="YOUR_PRIVATE_KEY",
        rpc_url="https://api.mainnet-beta.solana.com" #example URL
    )

    # Example usage: Resolve a domain
    domain_to_resolve = "bonfida.sol"
    resolved_domain = AllDomainsManager.resolve_all_domains(agent, domain_to_resolve)

    if resolved_domain:
        print(f"Domain {domain_to_resolve} resolves to: {resolved_domain}")
    else:
        print(f"Could not resolve domain {domain_to_resolve}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Helius NFT support: Get rich information using Helius
```python
import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_helius import HeliusManager
import json

async def main():
        PRIVATE_KEY = ""  # DO NOT commit this to version control!
        RPC_URL = "https://api.devnet.solana.com"
        HELIUS_API_KEY = "YOUR_VALID_HELIUS_KEY"  
        quicknode_rpc_url = ""
        openai_api_key = ""  

        agent = SolanaAgentKit(
            private_key=PRIVATE_KEY,
            rpc_url=RPC_URL,
            helius_api_key=HELIUS_API_KEY,
            quicknode_rpc_url = quicknode_rpc_url,
            openai_api_key = openai_api_key
        )

        # Sample list of mint accounts to fetch metadata for
        mint_accounts = [
            "6Q5mU3m6yE38tD6G5y664j7Q3Q5yS96Y819573k9zJ9R" #Example
        ]

        try:
            # Get NFT metadata
            nft_metadata_result = HeliusManager.get_nft_metadata(agent, mint_accounts)
            print("\nNFT Metadata:")
            print(json.dumps(nft_metadata_result, indent=4)) 
        except Exception as e:
            print(f"Error getting NFT metadata: {e}")

if __name__ == "__main__":
        asyncio.run(main())
```

## Request Faucet Funds: Useful for testing purposes.
```python
import asyncio
from agentipy.tools.request_faucet_funds import FaucetManager
from agentipy.agent import SolanaAgentKit

async def request_devnet_funds():
    agent = SolanaAgentKit(
        private_key="",  # Replace with your private key
        rpc_url="https://api.devnet.solana.com" #example URL
    )

    txn_sig = await FaucetManager.request_faucet_funds(agent)
    print(f"TX: {txn_sig}")

if __name__ == "__main__":
        asyncio.run(request_devnet_funds())
```

## Authenticate Wallet on CyberProtocol and create a Coin: A easy example.
```python
import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_cybers import CybersManager

async def main():
    private_key = ""  # Replace with your private key (DO NOT COMMIT!)

    agent = SolanaAgentKit(private_key=private_key, rpc_url="https://api.devnet.solana.com") #example URL

    try:
        #Authenticate
        jwt_token = CybersManager.authenticate_wallet(agent)
        if jwt_token:
            print(f"Successfully authenticated with Cybers. JWT token: {jwt_token[:50]}...")  #Show that authentication is working
        else:
            print("Failed to authenticate with Cybers.")
            return

        # Creating Coin
        image_path = ""

        create_coin_response = CybersManager.create_coin(
            agent=agent,
            name="test_coin", 
            symbol="TEST",
            image_path=image_path, 
            tweet_author_id="1234567890", 
            tweet_author_username="Test_account"
        )

        if create_coin_response:
            print(f"Coin creation successful. Mint address: {create_coin_response.get('mintAddress')}")
        else:
            print("Failed to create coin.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Drift Protocol User Creation Example: Useful to automate actions related to drift on testnet.
```python
import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_drift import DriftManager

async def create_drift_account():
    # Replace with your actual values and keys
    PRIVATE_KEY = "" # Your Mainnet-beta private key
    RPC_URL = "https://api.mainnet-beta.solana.com" #example URL
    DRIFT_PROGRAM_ID = "your_drift_program_id" #replace with drift program id.
    OPEN_API_KEY = "" # replace with Open-AI Key

    agent = SolanaAgentKit(private_key=PRIVATE_KEY, rpc_url=RPC_URL, drift_program_id = DRIFT_PROGRAM_ID, openai_api_key = OPEN_API_KEY)

    DEPOSIT_AMOUNT = 0.01 # Deposit amount in USDC
    DEPOSIT_SYMBOL = "USDC" # Deposit symbol

    try:
        #Create a Drift user account
        create_account_result = DriftManager.create_drift_user_account(agent, DEPOSIT_AMOUNT, DEPOSIT_SYMBOL)

        if create_account_result["success"]:
            print(f"Drift account created successfully!")
            print(f"Transaction: {create_account_result['transaction']}")
        else:
            print("Failed to create Drift account:")
            print(f"Error: {create_account_result['error']}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(create_drift_account())
```


## 🆕 New Tool Examples

This section provides examples of how to use the new `CoingeckoManager` and `token_price_trader` tools.

### Example 1: Using `CoingeckoManager` to Fetch Market Data

This example demonstrates fetching trending tokens, token price data, and other market metrics using the `CoingeckoManager`.

```python
# coingecko_example.py
import aiohttp
import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_coingecko import CoingeckoManager

async def coingecko_example():
    #Replace these with your actual values and keys
    PRIVATE_KEY = ""
    RPC_URL = "https://api.mainnet-beta.solana.com"
    COINGECKO_API_KEY = "your_valid_pro_api_key_here"
    COINGECKO_DEMO_API_KEY = ""

    agent = SolanaAgentKit(
        private_key=PRIVATE_KEY,
        rpc_url=RPC_URL,
        coingecko_api_key=COINGECKO_API_KEY,
        coingecko_demo_api_key=COINGECKO_DEMO_API_KEY
    )

    token_address = "So11111111111111111111111111111111111111112"  # SOL
    token_address_list = [token_address]

    try:
        trending_tokens_data = await CoingeckoManager.get_trending_tokens(agent)
        print("\nTrending Tokens Data:")
        print(trending_tokens_data)
    except Exception as e:
        print(f"Error with trending tokens: {e}")

    try:
        token_price_data = await CoingeckoManager.get_token_price_data(agent, token_address_list)
        print("\nToken Price Data:")
        print(token_price_data)
    except Exception as e:
        print(f"Error with token price data: {e}")

    try:
        trending_pools_data = await CoingeckoManager.get_trending_pools(agent)
        print("\nTrending Pools Data:")
        print(trending_pools_data)
    except Exception as e:
        print(f"Error with trending pools: {e}")

    try:
        top_gainers_data = await CoingeckoManager.get_top_gainers(agent)
        print("\nTop Gainers Data:")
        print(top_gainers_data)
    except Exception as e:
        print(f"Error with top gainers: {e}")

    try:
        token_info_data = await CoingeckoManager.get_token_info(agent, token_address)
        print("\nToken Info Data:")
        print(token_info_data)
    except Exception as e:
        print(f"Error with token info: {e}")

    try:
        latest_pools_data = await CoingeckoManager.get_latest_pools(agent)
        print("\nLatest Pools Data:")
        print(latest_pools_data)
    except Exception as e:
        print(f"Error with latest pools: {e}")

if __name__ == "__main__":
    asyncio.run(coingecko_example())
```

Brief Explanation: This example uses CoingeckoManager to fetch and print data. It uses SolanaAgentKit to abstract away the underlying RPC calls. Replace the placeholder API keys with your actual CoinGecko API keys (free and/or pro).

### Example 2: Using token_price_trader for Automated Trading

This example provides a more comprehensive, self-contained demo to illustrate the TokenTrader tool. It includes:

Price Fetching: Fetches token prices from Jupiter, Raydium, and DEX Screener.

Balance Check: Checks SOL and token balances.

Trade Execution: Allows the user to buy or sell tokens based on fetched prices, using the TradeManager and Jupiter.

```python
# token_price_trader.py
import asyncio
import aiohttp
from solders.pubkey import Pubkey
from agentipy.agent import SolanaAgentKit
from agentipy.tools.get_token_data import TokenDataManager
from agentipy.tools.trade import TradeManager
from agentipy.tools.get_balance import BalanceFetcher
from spl.token.async_client import AsyncToken
from spl.token.constants import TOKEN_PROGRAM_ID

# Known Solana Mint Addresses
SOL_MINT = Pubkey.from_string("So11111111111111111111111111111111111111112")  # Wrapped SOL
USDC_MINT = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")  # USDC on Solana
WBTC_MINT = Pubkey.from_string("3NZ9JMVBmGAqocybic2c7LQCJScmgsAZ6vQqTDzcqmJh")  # Wrapped BTC on Solana
JUP_MINT = Pubkey.from_string("JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN")  # JUP token

JUP_API = "https://quote-api.jup.ag/v6"  #
RAYDIUM_API = "https://api.raydium.io/v2/main/price"
DEXSCREENER_API = "https://api.dexscreener.com/latest/dex/tokens/"
SLIPPAGE_BPS = 50
PROBE_AMOUNT = 1 * 10**8  # 0.1 SOL in lamports for smaller probes
PROBE_AMOUNT_JUP = 1 * 10**6  # 0.000001 SOL (very small for JUP liquidity)

# Initialize SolanaAgentKit for mainnet
agent = SolanaAgentKit(
    private_key="",  # Replace with your mainnet private key
    rpc_url="https://api.mainnet-beta.solana.com"  # Mainnet RPC endpoint
)

async def get_jupiter_quote(session, input_mint, output_mint, amount, retries=3):
    """Fetch price quote from Jupiter v6 API."""
    url = (
        f"{JUP_API}/quote?"
        f"inputMint={input_mint}&outputMint={output_mint}&amount={amount}"
        f"&slippageBps={SLIPPAGE_BPS}"
    )
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                # print(f"Jupiter Quote URL: {url}")
                if response.status == 404:
                    print(f"Jupiter: No quote available for {input_mint} -> {output_mint}")
                    return None
                if response.status != 200:
                    # print(f"Jupiter: Error fetching quote: HTTP {response.status}")
                    return None
                data = await response.json()
                # print(f"Jupiter Quote response: {data}")
                return data
        except Exception as e:
            # print(f"Jupiter: Network error on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(1)
    return None

async def get_raydium_price(session, token_mint):
    """Fetch price from Raydium’s price endpoint."""
    try:
        async with session.get(RAYDIUM_API) as response:
            if response.status != 200:
                print(f"Raydium: Error fetching price: HTTP {response.status}")
                return None
            data = await response.json()
            price = data.get(str(token_mint))
            if price:
                print(f"Raydium: Found price for {token_mint}: {price} SOL")
                return float(price)
            print(f"Raydium: No price found for {token_mint}")
            return None
    except Exception as e:
        print(f"Raydium: Network error fetching price: {e}")
        return None

async def get_dexscreener_price(session, token_mint):
    """Fetch price from DEX Screener for Solana pairs, focusing on Orca and Raydium."""
    url = f"{DEXSCREENER_API}{token_mint}"
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"DEX Screener: Error fetching price: HTTP {response.status}")
                return None
            data = await response.json()
            if not data.get("pairs"):
                print(f"DEX Screener: No pairs found for {token_mint}")
                return None
            sol_pairs = [pair for pair in data["pairs"] if pair["chainId"] == "solana" and pair["quoteToken"]["address"] == str(SOL_MINT)]
            prices = {}
            for pair in sol_pairs:
                dex = pair.get("dexId", "Unknown")
                if dex in ["raydium", "orca"]:
                    price_sol = float(pair.get("priceNative", 0))
                    if price_sol > 0 and 0.001 < price_sol < 10:
                        prices[dex] = price_sol
            return prices if prices else None
    except Exception as e:
        print(f"DEX Screener: Network error fetching price: {e}")
        return None

async def get_token_decimals(mint):
    """Fetch token decimals from RPC, defaulting to 9 if unavailable."""
    decimals = 9  # Default for Wrapped SOL
    if str(mint) != str(SOL_MINT):
        try:
            token = AsyncToken(agent.connection, mint, TOKEN_PROGRAM_ID, agent.wallet)
            mint_info = await token.get_mint_info()
            if mint_info is not None:
                decimals = mint_info.decimals
            else:
                print(f"No mint info for {mint}, assuming 9 decimals")
        except Exception as e:
            print(f"Failed to fetch decimals for {mint}: {e}, assuming 9 decimals")
    return decimals

async def fetch_token_prices(ticker):
    """Fetch current prices for a token across Jupiter, Raydium, and DEX Screener (Orca, Raydium)."""
    ticker = ticker.upper()
    if ticker == "SOL":
        print("SOL is the native currency. Price is 1 SOL per SOL.")
        return {"N/A": 1.0}, SOL_MINT, 9
    elif ticker == "USDC":
        token_mint = USDC_MINT
    elif ticker == "BTC":
        token_mint = WBTC_MINT
    elif ticker == "JUP":
        token_mint = JUP_MINT
    else:
        try:
            token_data = TokenDataManager.get_token_data_by_ticker(ticker)
            if token_data and token_data.address:
                token_mint = Pubkey.from_string(token_data.address)
                print(f"Resolved mint for {ticker}: {token_mint}")
            else:
                print(f"No Solana token found for '{ticker}'. Try SOL, USDC, BTC, or JUP.")
                return None, None, None
        except Exception as e:
            print(f"Error resolving '{ticker}': {e}")
            return None, None, None

    decimals = await get_token_decimals(token_mint)
    print(f"Decimals fetched: {decimals}")

    prices = {}
    async with aiohttp.ClientSession() as session:
        # Jupiter Price (SOL -> Token)
        amount = PROBE_AMOUNT if ticker not in ["JUP"] else PROBE_AMOUNT_JUP
        jupiter_quote = await get_jupiter_quote(session, SOL_MINT, token_mint, amount)
        if jupiter_quote and "outAmount" in jupiter_quote:
            token_amount = int(jupiter_quote["outAmount"]) / 10**decimals
            prices["Jupiter"] = (PROBE_AMOUNT if ticker not in ["JUP"] else PROBE_AMOUNT_JUP) / 10**9 / token_amount

        # Raydium Price
        raydium_price = await get_raydium_price(session, token_mint)
        if raydium_price:
            prices["Raydium"] = raydium_price

        # DEX Screener Prices (Orca and Raydium only)
        dexscreener_prices = await get_dexscreener_price(session, token_mint)
        if dexscreener_prices:
            prices.update(dexscreener_prices)

    return prices, token_mint, decimals

async def check_balance(token_mint=None):
    """Check wallet balances, handling missing token accounts."""
    sol_balance = await BalanceFetcher.get_balance(agent)
    token_balance = 0
    if token_mint:
        if str(token_mint) == str(SOL_MINT):
            token_balance = sol_balance
        else:
            try:
                token_balance = await BalanceFetcher.get_balance(agent, token_mint)
            except Exception as e:
                print(f"Error fetching token balance: {e}")
                token_balance = 0
    print(f"Wallet Balances: SOL = {sol_balance or 0:.7f}, Token = {token_balance or 0:.7f}")
    return sol_balance, token_balance

async def trade_token(ticker):
    """Handle trading logic for a given token ticker."""
    print(f"\nFetching prices for {ticker}...")
    prices, token_mint, decimals = await fetch_token_prices(ticker)

    if not prices:
        print(f"No prices available for {ticker} on Solana DEXs.")
    else:
        print("\nCurrent Prices (SOL per token):")
        for dex, price in prices.items():
            print(f"  {dex}: {price:.7f} SOL")

    sol_balance, token_balance = await check_balance(token_mint)

    action = input("\nEnter action (buy/sell/exit): ").lower()
    if action == "exit":
        return
    elif action not in ["buy", "sell"]:
        print("Invalid action.")
        return

    dex = input("Enter DEX (e.g., Jupiter, Raydium, Orca): ").capitalize()
    if dex not in prices:
        print(f"No price available on {dex}.")
        return

    amount = float(input("Enter amount (in tokens): "))
    if amount <= 0:
        print("Invalid amount.")
        return

    if action == "buy":
        sol_amount = amount * prices[dex]
        if sol_balance < sol_amount:
            print("Insufficient SOL balance.")
            return
        print(f"Buying {amount:.7f} {ticker} for {sol_amount:.7f} SOL on {dex}")
        signature = await TradeManager.trade(
            agent=agent,
            output_mint=token_mint,
            input_amount=sol_amount,
            input_mint=SOL_MINT,
            slippage_bps=SLIPPAGE_BPS
        )
        print(f"Trade successful: https://explorer.solana.com/tx/{signature}")
    elif action == "sell":
        if token_balance < amount:
            print("Insufficient token balance.")
            return
        expected_sol = prices[dex] * amount
        print(f"Selling {amount:.7f} {ticker} for ~{expected_sol:.7f} SOL on {dex}")
        signature = await TradeManager.trade(
            agent=agent,
            output_mint=SOL_MINT,
            input_amount=amount,
            input_mint=token_mint,
            slippage_bps=SLIPPAGE_BPS
        )
        print(f"Trade successful: https://explorer.solana.com/tx/{signature}")

    await check_balance(token_mint)

async def main():
    print("Starting Solana Token Price Trader on Mainnet...")
    while True:
        ticker = input("\nEnter token ticker (or 'quit' to exit): ").upper()
        if ticker == "QUIT":
            break
        await trade_token(ticker)

if __name__ == "__main__":
    asyncio.run(main())
```

## 💡 Advanced Features and Best Practices

AgentiPy supports custom protocol creation, as well as integrations with Langchain and Base tools, enabling you to extend functionality and build powerful AI-driven dApps.

**1. Custom Protocol Creation:**

```python
from agentipy.base import ProtocolBase
from agentipy.solana import SolanaClient

class MyProtocol(ProtocolBase):
    def custom_action(self):
        pass

solana = SolanaClient(private_key="your_private_key_here")  # Replace with secure key management
solana.add_protocol(MyProtocol())
```

**2. Langchain Integration:**
AgentiPy can be seamlessly integrated with Langchain, a powerful framework for building language model-powered applications. This enables you to create intelligent agents that can understand natural language instructions, reason about blockchain data, and execute complex on-chain actions.

* Natural Language Command Interpretation: Use Langchain's language models (LLMs) to parse user instructions and map them to AgentiPy tool calls.

* Dynamic Workflow Generation: Design agents that can dynamically chain together multiple AgentiPy tools to accomplish complex goals.

* Enhanced Decision-Making: Leverage LLMs to analyze blockchain data (e.g., token prices, market conditions) and make intelligent trading or DeFi decisions.

Example (Illustrative):
```python
from langchain.llms import OpenAI  # Or any other Langchain LLM
from agentipy.agent import SolanaAgentKit
from agentipy.tools.trade import TradeManager

# Initialize Langchain LLM
llm = OpenAI(openai_api_key="YOUR_OPENAI_API_KEY")  # Replace with your OpenAI API key
agent = SolanaAgentKit(
    private_key="YOUR_PRIVATE_KEY",
    rpc_url="https://api.mainnet-beta.solana.com"
)

# Define a trading prompt
prompt = "Buy 1 SOL of USDC"

# Example - Basic text prompt (replace with more sophisticated agent logic)
action = llm(prompt)  # Get action from the language model

# Simplified trade example
try:
    TradeManager.trade(
        agent=agent,
        output_mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", #USDC on Solana mainnet
        input_amount=0.1
    )  # Simplified trade example
    print(f"Performed action: {action}")
except Exception as e:
    print(f"Error processing trade: {e}")
```

**3. Using Base Tools:**
* Use Base tools and functions to have a better management
```python
from agentipy.base import BaseClient

# Replace with your private key (DO NOT HARDCODE IN PRODUCTION - use environment variables!)
base = BaseClient()

#Create a wallet
new_wallet = base.create_wallet()
print(f"Wallet address: {new_wallet.address} and Private Key: {new_wallet.privateKey}")

# Get base balance
balance = base.get_balance("your_wallet_address")
print(f"Balance: {balance} base")

# Transfer 1 base to a recipient
transaction = base.transfer_base(to_address="recipient_wallet_address", amount=1.0)
print("Transaction Successful {transaction.hash}")
```

Error handling is crucial for robust applications:
```python
try:
    solana.transfer_sol(to_address="invalid_address", amount=1.0)
except ValueError as e:
    print(f"Error: {e}")
```

### 🤝  Community Engagement and Contribution
AgentiPy encourages community contributions, with developers invited to fork the repository at [github.com/niceberginc/agentipy/](https://github.com/niceberginc/agentipy/), submit pull requests, and report issues via GitHub Issues. This collaborative approach fosters continuous improvement and innovation within the ecosystem.

#### 📜 Licensing and Contact Information
AgentiPy is licensed under the MIT License, ensuring open access and flexibility for developers. For support, contact [support@agentipy.com](mailto:support@agentipy.com), follow updates on X at [@AgentiPy](https://x.com/AgentiPy), or join the community on Discord at [Join our Discord Community](https://discord.com/invite/agentipy).



