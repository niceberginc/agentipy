# Solana Arbitrage Trading Bot

This project implements an arbitrage trading bot for the Solana blockchain, leveraging the power of `agentipy` and `LangChain` to automate the process. The bot identifies and exploits arbitrage opportunities across different decentralized exchanges (DEXs) on Solana.

## Overview

This bot uses `agentipy` to interact with the Solana blockchain, providing tools for fetching token prices, checking balances, and executing trades. `LangChain` is used to create an agent that analyzes market data, makes trading decisions, and interacts with the user.

## Technologies Used

*   **Python:** The primary programming language.
*   **`agentipy`:** A library that simplifies interaction with the Solana blockchain, providing tools for common actions such as fetching prices, managing wallets and transactions, and trading.
*   **`LangChain`:** A framework for developing applications powered by large language models (LLMs).  It's used here for creating an agent to make trading decisions and interact with the user.
*   **`aiohttp`:** An asynchronous HTTP client for making API requests to DEXs and CoinGecko.
*   **`solders`:**  A library for working with Solana data structures (Pubkeys, etc.).
*   **`openai`:** For the Google Gemini LLM.
*   **`python-dotenv`:** To load environment variables from a `.env` file for securely managing API keys and private keys.

## Key Components & Their Roles

1.  **`agentipy` & Solana Interaction:**

    *   `SolanaAgentKit`: This is your core interface to the Solana blockchain.  It manages your wallet (using the provided private key), connects to the Solana RPC endpoint, and provides methods for interacting with the chain.
    *   The bot utilizes the following `agentipy` tools:
        *   `SolanaTradeTool`:  (Most Important) Executes a token trade on a specified DEX (e.g., Jupiter, Orca, Raydium). The agent uses this tool to buy and sell tokens.
        *   `BalanceFetcher.get_balance`: Used to fetch the SOL and token balances for making correct trading decisions.
        *   `TradeManager.trade`: Executes the trade.
        *   `TokenDataManager.get_token_data_by_ticker`: Resolves ticker symbols to token mint addresses.
        *   `AsyncToken`: Used to get token details.
    *   (Note: The bot will utilize other relevant Agentipy tools as specified in the code.

2.  **`LangChain` Agent:**

    *   `ChatGoogleGenerativeAI`: The LLM is responsible for analyzing data and generating trading decisions.
    *   `PromptTemplate`:  Defines the instructions and context given to the LLM to make trading decisions.
    *   `LLMChain`: Creates a chain that combines the LLM with a trading prompt.
    *   **The agent performs these steps:**
        1.  Fetches the trending tokens from CoinGecko.
        2.  Presents a list of trending tokens to the user or takes a custom ticker.
        3.  Fetches prices for the selected token on different DEXs using `fetch_token_prices()`.
        4.  Checks the wallet balance for the token.
        5.  Uses the LLM chain to make a buy/sell decision based on the price data and balance.
        6.  Prompts the user to confirm the trade before execution.
        7.  Executes the trade if confirmed (using Agentipy tools).

3.  **Price Data & Arbitrage Logic:**

    *   **Price Fetching:** The bot fetches token prices from multiple DEXs. The goal is to find an arbitrage opportunity -- buying a token on one DEX and selling it on another at a higher price, to make a profit.
    *   **Fee Consideration:** The trading prompt instructs the LLM to take transaction fees and other costs (e.g., potential ATA rent) into account.
    *   **User Confirmation:** Before every trade, the bot asks the user for confirmation, protecting against errors or unintended trades.

## Setup and Usage

1.  **Install Dependencies:**

    ```bash
    pip install agentipy aiohttp solders langchain langchain_google_genai python-dotenv
    ```

2.  **Set up the .env file:**

    *   Create a file named `.env` in the same directory as your Python script.
    *   Add the following lines to the `.env` file:

        ```
        GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY  # Your Google Gemini API key
        PRIVATE_KEY=YOUR_SOLANA_PRIVATE_KEY  # Your Solana wallet's private key (export this safely)
        ```

    *   **Important:** *Never* commit your `.env` file to version control (e.g., Git). Add it to your `.gitignore` file.
    *   For the `PRIVATE_KEY`, you will need to *export* it in your terminal, so the script can load it.  You can use the `export` command in Linux/macOS or set an environment variable in Windows.  For example:

        ```bash
        # Linux/macOS (in your terminal, *before* running the script):
        export PRIVATE_KEY="YOUR_SOLANA_PRIVATE_KEY"
        ```

3.  **Run the Script:**

    ```bash
    python arbitrage.py
    ```

4.  **Interacting with the Bot:**

    *   The bot will first display a list of trending tokens.
    *   You can either:
        *   Enter the *number* corresponding to a trending token to trade that token.
        *   Enter the *ticker symbol* of a token you want to trade directly.
        *   Type `quit` to exit.
    *   The bot will then fetch price information, ask you to buy/sell and confirm the trade.
    *   Follow the prompts to complete the trading process.

## Tool Descriptions

The following table lists the LangChain tool descriptions:

| Tool Name                               | Description                                                                                                                      |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| `get_token_prices`                     | Fetches the price of a given token and returns price data from multiple DEXes such as Jupiter, Raydium and DEX Screener. It returns prices in SOL, as that is what is relevant to the Solana ecosystem.         |
| `check_balance`                        | Checks the SOL and token balances.                                                                                          |
| `trade_token`                         | Executes a token trade on a specified DEX.                                                                                             |
| `CoingeckoGetTrendingTokensTool`         | Fetches trending tokens from CoinGecko.                                                     |
| `fetch_token_prices`                       | Fetches current prices for a token across Jupiter, Raydium, and DEX Screener (Orca, Raydium).          |
| `get_trending_tokens`                    | Fetches trending tokens from CoinGecko *with USD prices*.     |

## Important Notes

*   **Security:**
    *   **Protect your private key!**  Never hardcode your private key directly in the code.  Use environment variables, secure key vaults, or other secure methods.
    *   **Review code before use:**  Carefully review and understand the code before running it with real funds.
*   **Risk:** Trading cryptocurrencies carries significant risk.  This bot is for informational and educational purposes only and should not be considered financial advice. Always trade responsibly and only with funds you can afford to lose.
*   **Rate Limits:** Be aware of API rate limits. Implement retries and delays as needed, especially when using the OpenAI API.
*   **Slippage:** Carefully consider slippage tolerance.
*   **Testing:**  Thoroughly test the bot in a test environment (e.g., Solana's devnet) before using it with real funds on the mainnet.
*   **API Keys:**  Ensure your API keys (OpenAI, etc.) are valid, and that you have sufficient quota/credits.
*   **Token Addresses:** The code uses hardcoded addresses and resolves tickers to addresses.  A token registry would make the code more robust.
*   **Fees:** Account for transaction fees in all calculations, which are defined as `FEE_PER_TRADE`.  Also take into account rent for token accounts in any new trade operations.

## Disclaimer

This bot is provided "as is" without any warranty. The developer is not responsible for any losses incurred through its use. Use at your own risk.
