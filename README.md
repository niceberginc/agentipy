# AgentiPy: Your AI Agent Toolkit for Blockchain Applications

AgentiPy is a Python toolkit designed to empower AI agents to interact seamlessly with blockchain applications, focusing on Solana and Base. It simplifies the development of decentralized applications (dApps) by providing tools for token management, NFT handling, and more. With a focus on ease of use and powerful functionality, AgentiPy allows developers to create robust and sophisticated blockchain-based solutions, leveraging AI-driven workflows.



[<img src="https://img.shields.io/github/stars/niceberginc/agentipy?style=social" alt="GitHub Stars">](https://github.com/niceberginc/agentipy)
[<img src="https://img.shields.io/github/forks/niceberginc/agentipy?style=social" alt="GitHub Forks">](https://github.com/niceberginc/agentipy)
[<img src="https://static.pepy.tech/personalized-badge/agentipy?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Total Downloads">](https://pypi.org/project/agentipy/)
[<img src="https://img.shields.io/pypi/v/agentipy.svg" alt="PyPI Version">](https://pypi.org/project/agentipy/)
[<img src="https://img.shields.io/github/issues/niceberginc/agentipy" alt="Open Issues">](https://github.com/niceberginc/agentipy/issues)
[<img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python Version">](https://pypi.org/project/agentipy/)
[<img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">](https://github.com/niceberginc/agentipy/blob/main/LICENSE.md)
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
*   **Model Context Protocol (MCP) Support:** Includes a built-in MCP server module and supports integration with dedicated MCP servers (like the agentipy-mcp for Claude Desktop) for standardized AI interaction.

## 📦 Installation and Setup

Before you begin, ensure you have the following prerequisites:

*   **Python 3.8+:** Required for running the toolkit.
*   **Solana CLI:** For Solana-specific actions (e.g., wallet creation).
*   **Langchain:** For AI integration (`pip install langchain`).
*   **Wallet with Private Keys:**  Crucial for signing and sending transactions.  **Securely manage your private keys!**
*   **API Keys (Optional):** For accessing various blockchain networks or external data sources (e.g., CoinGecko, Allora, e.t.c.).

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
| Lulo           | Solana     | Lend assets to earn interest, Withdraw tokens           | [Lulo Lend Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_lulo.py) |
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
| StakeWithJup    | Solana     | Stakes JUP to earn JUP tokens                 | [Stake With Jup tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/stake_with_jup.py) |
|ThreeLand    | Solana     | ThreeLand NFT mint and deploy        | [ThreeLand NFT mint tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_3land.py) |
| ThreeLand    | Solana     | ThreeLand NFT mint and deploy        | [ThreeLand NFT mint tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_3land.py) |
| Elfa AI       | Solana     | Get trending tokens, mentions, smart account stats              | [Elfa AI Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_elfa_ai.py) |
| FluxBeam      | Solana     | Create a new pool                                               | [FluxBeam Tool](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_fluxbeam.py) |
| Agentipy MCP          | Solana     | Extensible Solana toolset via a Model Context Protocol server       | [MCP tool](https://github.com/niceberginc/agentipy/tree/main/agentipy/mcp)             |
| Claude Desktop MCP    | Solana     | Claude‐compatible MCP server exposing onchain actions | [Agentipy MCP Server for Claude Desktop](https://github.com/niceberginc/agentipy-mcp) |





## 🚀 Quick Start Example


Important Security Note: Never hardcode your private key directly into your code. Use environment variables or secure key management systems in a production environment.


## Transfer SOL/SPL: Easily send tokens.
```python
from agentipy.agent import SolanaAgentKit
from agentipy.tools.transfer import TokenTransferManager
import asyncio

async def main():
    """
    Quick Start Example: Transfer SOL on Mainnet.
    """
    # **!!! IMPORTANT SECURITY WARNING !!!**
    # NEVER hardcode your private key directly into your code, ESPECIALLY for Mainnet.
    # This is for demonstration purposes ONLY.
    # In a real application, use environment variables, secure key vaults, or other
    # secure key management practices.  Compromising your private key can lead to
    # loss of funds.

    PRIVATE_KEY = ""  # ⚠️ REPLACE THIS SECURELY! ⚠️
    RECIPIENT_WALLET_ADDRESS = "" # 👤 REPLACE THIS WITH RECIPIENT ADDRESS 👤

    agent = SolanaAgentKit(
        private_key=PRIVATE_KEY,
        rpc_url="https://api.mainnet-beta.solana.com"  # Mainnet RPC endpoint
    )

    TRANSFER_AMOUNT_SOL = 0.0001 # A very small amount of SOL for testing.  Adjust as needed.

    try:
        transfer_signature = await TokenTransferManager.transfer(
            agent=agent,
            to=RECIPIENT_WALLET_ADDRESS,
            amount=TRANSFER_AMOUNT_SOL
        )
        print(f"Transfer successful!")
        print(f"Transaction Signature: https://explorer.solana.com/tx/{transfer_signature}")

    except RuntimeError as e:
        print(f"Error: Transfer failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())

```
## Checking Sol Balance Using Agentipy
```python
from agentipy.agent import SolanaAgentKit
from agentipy.tools.get_balance import BalanceFetcher
import asyncio

async def main():
    """
    Quick Start Example: Get SOL Balance on Mainnet.
    """
    # **Important Security Note:**
    # NEVER hardcode your private key directly into your code.
    # Use environment variables or secure key management systems in production.
    PRIVATE_KEY = "YOUR_PRIVATE_KEY_HERE"  # Replace with your actual private key (securely!)
    WALLET_ADDRESS = "YOUR_WALLET_ADDRESS_HERE" # Replace with your actual wallet address

    agent = SolanaAgentKit(
        private_key=PRIVATE_KEY,
        rpc_url="https://api.mainnet-beta.solana.com"  # Mainnet RPC endpoint
    )

    try:
        balance_sol = await BalanceFetcher.get_balance(agent)
        print(f"Wallet Balance for {WALLET_ADDRESS}: {balance_sol:.4f} SOL")
        print("Successfully retrieved SOL balance!")

    except Exception as e:
        print(f"Error: Could not retrieve SOL balance: {e}")

if __name__ == "__main__":
    asyncio.run(main())

```
## CoinGecko Market Data Metrics & Trending Tokens
```python
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_coingecko import CoingeckoManager
from agentipy.tools.get_token_data import TokenDataManager
from solders.pubkey import Pubkey
import asyncio

async def main():
    """
    Quick Start Example:
    1. Fetch Trending Tokens from CoinGecko.
    2. Fetch and display data metrics for a user-specified token ticker.
    """

    agent = SolanaAgentKit(
        private_key="",  # Private key not needed for this example
        rpc_url="https://api.mainnet-beta.solana.com"
    )

    # -------------------------------------------------------------
    # Section 1: Fetch and Display Trending Tokens (No API key needed)
    # -------------------------------------------------------------
    try:
        trending_tokens_data = await CoingeckoManager.get_trending_tokens(agent)

        if trending_tokens_data and 'coins' in trending_tokens_data:
            print("Trending Tokens on CoinGecko:")
            for token in trending_tokens_data['coins']:
                print(f"- {token['item']['symbol']} ({token['item']['name']})")
            print("\nSuccessfully fetched trending tokens!\n" + "-" * 40)
        else:
            print("No trending tokens data received.\n" + "-" * 40)

    except Exception as e:
        print(f"Error fetching trending tokens: {e}\n" + "-" * 40)

    # -------------------------------------------------------------
    # Section 2: Fetch and Display Data Metrics for User-Specified Token Name and vs Currency
    # -------------------------------------------------------------
    btc_price_data_usd = await agentEvm.get_coin_price_vs(["bitcoin"], ["usd"])

    btc_price_data_multi_vs = await agentEvm.get_coin_price_vs(["bitcoin"], ["usd,eur"])

    multiple_price_data = await agent.get_coin_price_vs(["bitcoin","solana","agentipy"], ["usd"])

    btc_info = btc_price_data_usd["bitcoin"]
    print(f"- Current Price (USD): ${btc_info['usd']:.4f}")
    print(f"- Market Cap (USD): ${btc_info['usd_market_cap']:.2f}")
    print(f"- 24h Volume (USD): ${btc_info['usd_24h_vol']:.2f}")
    print(f"- 24h Change (%): {btc_info['usd_24h_change']:.2f}%")
    print(f"- Last Updated: {btc_info['last_updated_at']}")
    print("\nSuccessfully fetched token data metrics!\n" + "-" * 40)

    # -------------------------------------------------------------
    # Section 3: Fetch and Display Data Metrics for User-Specified Ticker
    # -------------------------------------------------------------
    token_ticker = input("Enter a Token Ticker (e.g., SOL, USDC) to get its metrics: ").strip()

    if token_ticker:
        token_address = None
        try:
            resolved_address = TokenDataManager.get_token_address_from_ticker(token_ticker)
            if resolved_address:
                token_address = resolved_address
                print(f"Resolved ticker '{token_ticker}' to Contract Address: {token_address}")
            else:
                raise ValueError(f"Could not resolve ticker '{token_ticker}' to a Contract Address.")

            if token_address:
                price_data = await CoingeckoManager.get_token_price_data(agent, [token_address])

                if token_address in price_data and price_data[token_address]:
                    token_info = price_data[token_address]

                    print(f"\nData Metrics for {token_ticker.upper()} from CoinGecko:")
                    print(f"- Current Price (USD): ${token_info['usd']:.4f}")
                    print(f"- Market Cap (USD): ${token_info['usd_market_cap']:.2f}")
                    print(f"- 24h Volume (USD): ${token_info['usd_24h_vol']:.2f}")
                    print(f"- 24h Change (%): {token_info['usd_24h_change']:.2f}%")
                    print(f"- Last Updated: {token_info['last_updated_at']}")
                    print("\nSuccessfully fetched token data metrics!\n" + "-" * 40)

                else:
                    print(f"Could not retrieve price data for ticker: {token_ticker}.\n" + "-" * 40)

            else:
                print(f"Could not get token address for ticker: {token_ticker}.\n" + "-" * 40)


        except Exception as e:
            print(f"Error fetching data metrics for ticker '{token_ticker}': {e}\n" + "-" * 40)
    else:
        print("No token ticker entered.\n" + "-" * 40)

if __name__ == "__main__":
    asyncio.run(main())
```
## Jupiter Exchange SOL - USDC
```python
from agentipy.agent import SolanaAgentKit
from agentipy.tools.trade import TradeManager
from solders.pubkey import Pubkey
import asyncio

async def main():
    """
    Quick Start Example: Swap SOL for USDC on Jupiter Exchange .
    """
    # **!!! IMPORTANT SECURITY WARNING !!!**
    # NEVER hardcode your private key directly into your code, ESPECIALLY for Mainnet.
    # This is for demonstration purposes ONLY.
    # In a real application, use environment variables, secure key vaults, or other
    # secure key management practices.

    PRIVATE_KEY = "YOUR_PRIVATE_KEY_HERE"  # ⚠️ REPLACE THIS SECURELY! ⚠️

    agent = SolanaAgentKit(
        private_key=PRIVATE_KEY,
        rpc_url="https://api.mainnet-beta.solana.com"  # Mainnet RPC endpoint
    )

    # Mainnet Token Mint Addresses:
    USDC_MINT = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
    SOL_MINT = Pubkey.from_string("So11111111111111111111111111111111111111112")

    SWAP_AMOUNT_SOL = 0.0001

    try:
        print(f"Attempting to swap {SWAP_AMOUNT_SOL} SOL for USDC on Jupiter...")
        transaction_signature = await TradeManager.trade(
            agent=agent,
            output_mint=USDC_MINT,
            input_amount=SWAP_AMOUNT_SOL,
            input_mint=SOL_MINT
        )

        print(f"Swap successful!")
        print(f"Transaction Signature: https://explorer.solana.com/tx/{transaction_signature}")

        await asyncio.sleep(1)  # 1-second delay to help with rate limits due to RPC Delay

    except Exception as e:
        print(f"Error: Swap failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```
## Jupiter Exchange  USDC - SOL 
```python
from agentipy.agent import SolanaAgentKit
from agentipy.tools.trade import TradeManager
from solders.pubkey import Pubkey
import asyncio

async def main():
    """
    Quick Start Example: Swap SOL for USDC on Jupiter Exchange using AgentiPy.
    """
    # **!!! IMPORTANT SECURITY WARNING !!!**
    # NEVER hardcode your private key directly into your code, ESPECIALLY for Mainnet.
    # This is for demonstration purposes ONLY.
    # In a real application, use environment variables, secure key vaults, or other
    # secure key management practices.  Compromising your private key can lead to
    # loss of funds.

    PRIVATE_KEY = "YOUR_PRIVATE_KEY_HERE"  # ⚠️ REPLACE THIS SECURELY! ⚠️

    agent = SolanaAgentKit(
        private_key=PRIVATE_KEY,
        rpc_url="https://api.mainnet-beta.solana.com"  # Mainnet RPC endpoint
    )

    USDC_MINT = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")  # Mainnet USDC
    SOL_MINT = Pubkey.from_string("So11111111111111111111111111111111111111112")   # Mainnet SOL

    SWAP_AMOUNT_SOL = 0.0001  # A tiny amount of SOL to swap for USDC (adjust as needed)

    try:
        print(f"Attempting to swap {SWAP_AMOUNT_SOL} SOL for USDC on Jupiter...")
        transaction_signature = await TradeManager.trade(
            agent=agent,
            output_mint=USDC_MINT,  # output token is USDC (what you receive)
            input_amount=SWAP_AMOUNT_SOL, # Amount of input token (SOL)
            input_mint=SOL_MINT      # input token is SOL (what you send/give)
        )

        print(f"Swap successful!")
        print(f"Transaction Signature: https://explorer.solana.com/tx/{transaction_signature}")

    except Exception as e:
        print(f"Error: Swap failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

---
## Swap User-Specified Amount of SOL for User-Specified Token (Ticker or CA) 
```python
from agentipy.agent import SolanaAgentKit
from agentipy.tools.trade import TradeManager
from agentipy.tools.use_coingecko import CoingeckoManager
from agentipy.tools.get_token_data import TokenDataManager
from solders.pubkey import Pubkey
import asyncio

async def main():
    """
    Quick Start Example:
    1. Swap User-Specified Amount of SOL for User-Specified Token (Ticker or CA) on Jupiter.
    2. Fetch and display token data metrics from CoinGecko before swap confirmation.
    """
    # **!!! IMPORTANT SECURITY WARNING !!!**
    # NEVER hardcode your private key directly into your code, ESPECIALLY for Mainnet.
    # This is for demonstration purposes ONLY.
    # In a real application, use environment variables, secure key vaults, or other
    # secure key management practices.

    PRIVATE_KEY = "YOUR_PRIVATE_KEY_HERE"  # ⚠️ REPLACE THIS SECURELY! ⚠️

    agent = SolanaAgentKit(
        private_key=PRIVATE_KEY,
        rpc_url="https://api.mainnet-beta.solana.com"  # Mainnet RPC endpoint
    )

    USDC_MINT = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")  # Mainnet USDC
    SOL_MINT = Pubkey.from_string("So11111111111111111111111111111111111111112")   # Mainnet SOL

    # -------------------------------------------------------------
    # Section 1: Get User Input for Target Token and Swap Amount
    # -------------------------------------------------------------
    target_token_input = input("Enter Target Token Ticker (e.g., USDC, BONK) or Contract Address: ").strip()
    swap_amount_sol_input = input("Enter Amount of SOL to Swap: ").strip()

    target_token_address = None
    target_token_symbol = None
    swap_amount_sol = None

    try:
        swap_amount_sol = float(swap_amount_sol_input)
        if swap_amount_sol <= 0:
            raise ValueError("Swap amount must be greater than zero.")
    except ValueError:
        print("Invalid SOL amount entered. Please enter a positive number.")
        return  # Exit if swap amount is invalid


    try:
        # Try to parse as a Pubkey (Contract Address)
        Pubkey.from_string(target_token_input)
        target_token_address = target_token_input
        print(f"Interpreting input as Contract Address: {target_token_address}")
    except ValueError:
        # If not a valid Pubkey, assume it's a Ticker
        print(f"Interpreting input as Token Ticker: {target_token_input}")
        try:
            resolved_address = TokenDataManager.get_token_address_from_ticker(target_token_input)
            if resolved_address:
                target_token_address = resolved_address
                token_data = TokenDataManager.get_token_data_by_address(Pubkey.from_string(target_token_address))
                if token_data:
                    target_token_symbol = token_data.symbol
                else:
                    target_token_symbol = target_token_input.upper() # Fallback to ticker
                print(f"Resolved ticker '{target_token_input}' to Contract Address: {target_token_address}")
            else:
                raise ValueError(f"Could not resolve ticker '{target_token_input}' to a Contract Address.")
        except Exception as resolve_error:
            print(f"Error resolving ticker: {resolve_error}")
            print("Please ensure you entered a valid Token Ticker or Contract Address.")
            return  # Exit if ticker resolution fails

    if target_token_address and swap_amount_sol is not None:
        # -------------------------------------------------------------
        # Section 2: Fetch and Display Token Data Metrics from CoinGecko
        # -------------------------------------------------------------
        try:
            price_data = await CoingeckoManager.get_token_price_data(agent, [target_token_address])

            if target_token_address in price_data and price_data[target_token_address]:
                token_info = price_data[target_token_address]
                display_symbol = target_token_symbol if target_token_symbol else target_token_input.upper()

                print(f"\nData Metrics for {display_symbol} ({target_token_address}) from CoinGecko:")
                print(f"- Current Price (USD): ${token_info['usd']:.4f}")
                print(f"- Market Cap (USD): ${token_info['usd_market_cap']:.2f}")
                print(f"- 24h Volume (USD): ${token_info['usd_24h_vol']:.2f}")
                print(f"- 24h Change (%): {token_info['usd_24h_change']:.2f}%")
                print(f"- Last Updated: {token_info['last_updated_at']}")
                print("-" * 40)

                # -------------------------------------------------------------
                # Section 3: Confirm Swap with User
                # -------------------------------------------------------------
                confirmation = input(f"\nConfirm swap of {swap_amount_sol} SOL for {display_symbol}? (yes/no): ").lower()
                if confirmation == "yes":
                    try:
                        print(f"Attempting to swap {swap_amount_sol} SOL for {display_symbol} on Jupiter...")
                        transaction_signature = await TradeManager.trade(
                            agent=agent,
                            output_mint=Pubkey.from_string(target_token_address), 
                            input_amount=swap_amount_sol, 
                            input_mint=SOL_MINT
                        )

                        print(f"Swap successful!")
                        print(f"Transaction Signature: https://explorer.solana.com/tx/{transaction_signature}")
                        await asyncio.sleep(1) 

                    except Exception as swap_error:
                        print(f"Error: Swap failed: {swap_error}")
                else:
                    print("Swap cancelled by user.")

            else:
                print(f"Could not retrieve price data for {target_token_input} from CoinGecko.")
        except Exception as e:
            print(f"Error fetching token data metrics: {e}")
    else:
        print("No valid Token Ticker or Contract Address provided, or invalid swap amount.")

if __name__ == "__main__":
    asyncio.run(main())
```

# 2. Langchain Integration:
AgentiPy can be seamlessly integrated with Langchain, a powerful framework for building language model-powered applications. This enables you to create intelligent agents that can understand natural language instructions, reason about blockchain data, and execute complex on-chain actions.

* Natural Language Command Interpretation: Use Langchain's language models (LLMs) to parse user instructions and map them to AgentiPy tool calls.

* Dynamic Workflow Generation: Design agents that can dynamically chain together multiple AgentiPy tools to accomplish complex goals.

* Enhanced Decision-Making: Leverage LLMs to analyze blockchain data (e.g., token prices, market conditions) and make intelligent trading or DeFi decisions.

**Example:**
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

# Example - Basic text prompt 
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


# 3. Model Context Protocol (MCP) Integration

Agentipy includes a built-in MCP module (`agentipy/mcp`) to expose on-chain actions via the Model Context Protocol. This enables standardized tool invocation by AI agents.

### ALL_ACTIONS

```python
# agentipy/mcp/all_actions.py
from agentipy.mcp.allora import ALLORA_ACTIONS
from agentipy.mcp.core import SOLANA_ACTIONS
from agentipy.mcp.jupiter import JUPITER_ACTIONS

ALL_ACTIONS = {
    **SOLANA_ACTIONS,
    **ALLORA_ACTIONS,
    **JUPITER_ACTIONS,
}
```

### Core Solana Actions
- `GET_BALANCE`: Fetch wallet SOL/SPL balances.
- `TRANSFER`: Transfer SOL or SPL tokens.
- `DEPLOY_TOKEN`: Deploy a new SPL token.

Defined in `agentipy/mcp/core/__init__.py` using `BalanceFetcher`, `TokenTransferManager`, and `TokenDeploymentManager`.

### Allora Actions
- `GET_ALL_TOPICS`: List Allora inference topics.
- `GET_PRICE_PREDICTION`: Fetch BTC/ETH price predictions.
- `GET_INFERENCE_BY_TOPIC_ID`: Retrieve inference by topic ID.

Defined in `agentipy/mcp/allora` and backed by `AlloraManager`.

### Jupiter Actions
- `STAKE_WITH_JUP`: Stake SOL for JUP rewards.
- `TRADE_WITH_JUP`: Execute token swaps on Jupiter.

Defined in `agentipy/mcp/jupiter` using `StakeManager` and `TradeManager`.

### MCP Server

```python
# agentipy/mcp/mcp_server.py
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import Tool, TextContent
from agentipy.agent import SolanaAgentKit
from agentipy.mcp.all_actions import ALL_ACTIONS

# Initialize server with Solana tools
mcp = FastMCP(
    "agentipy-mcp",
    instructions="Solana tools: Get balance, transfer SOL, price prediction, etc.",
    dependencies=["pydantic", "httpx", "solana"],
)
# Functions to register, normalize kwargs, and run the server...
```

This server auto-registers all tools in `ALL_ACTIONS` and can be started via:

```python
from agentipy.agent import SolanaAgentKit
from agentipy.mcp.mcp_server import start_mcp_server, ALL_ACTIONS

agent = SolanaAgentKit(private_key="<KEY>", rpc_url="<RPC_URL>")
start_mcp_server(agent)  # Exposes all Solana, Allora, and Jupiter actions
```

---

## Agentipy MCP Server for Claude Desktop

A Model Context Protocol (MCP) server that provides on-chain tools for Claude AI, allowing it to interact with the Solana blockchain through a standardized interface. This implementation uses Agentipy and enables AI agents to perform blockchain operations seamlessly.


###  Claude Desktop Integration

**[Agentipy MCP Server](https://github.com/niceberginc/agentipy-mcp)** extends Claude's capabilities with blockchain tools:

```json
// Claude Desktop Configuration
{
  "mcpServers": {
    "agentipy": {
      "command": "./run_mcp.sh",
      "autoApprove": ["GET_BALANCE", "PRICE_PREDICTION"]
    }
  }
}
```

**Featured Tools:**
-  Balance checks
-  Cross-chain swaps (deBridge)
-  Pyth price feeds
-  CoinGecko analytics
-  AI-driven trading

[Explore our MCP Server full guide for Claude Desktop](https://github.com/niceberginc/agentipy-mcp)

## Security Considerations

- Keep private keys secure
- Use environment variables for sensitive data
- Test on devnet/testnet before mainnet


### 🤝  Community Engagement and Contribution
AgentiPy encourages community contributions, with developers invited to fork the repository at [github.com/niceberginc/agentipy/](https://github.com/niceberginc/agentipy/), submit pull requests, and report issues via GitHub Issues. This collaborative approach fosters continuous improvement and innovation within the ecosystem.

#### 📜 Licensing and Contact Information
AgentiPy is licensed under the MIT License, ensuring open access and flexibility for developers. For support, contact [support@agentipy.com](mailto:support@agentipy.com), follow updates on X at [@AgentiPy](https://x.com/AgentiPy), or join the community on Discord at [Join our Discord Community](https://discord.com/invite/agentipy).









### 👥 Contributors


<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

[Become a contributor!](https://github.com/niceberginc/agentipy/blob/main/CONTRIBUTING.md) Open an issue or submit a pull request to join us!













