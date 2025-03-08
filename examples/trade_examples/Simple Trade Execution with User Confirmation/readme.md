# AgentiPy Example: Simple Trade Execution with User Confirmation

This example demonstrates a basic trade execution flow using the AgentiPy library, specifically for swapping SOL for another token on the Solana blockchain. It includes user input, optional Coingecko price data retrieval, user confirmation, and trade execution using the Jupiter aggregator.

## Prerequisites

*   **Python 3.8+**: Ensure you have Python installed.
*   **AgentiPy**: Install the library using `pip install agentipy`.
*   **.env file**: Create a `.env` file in the same directory as `main.py` and include your Solana private key:

    ```
    SOLANA_PRIVATE_KEY="your_private_key"
    ```

    **Important Security Note:** Never hardcode your private key directly in your code.  Use environment variables as shown here, or a more secure key management system in a production environment.  Compromising your private key can lead to loss of funds.
*   **Environment Variables:** Set the `SOLANA_PRIVATE_KEY` environment variable to your Solana private key.  This is handled by the `load_dotenv()` function in the code.
*   **Network Connection**: You need a reliable internet connection to connect to the Solana RPC.

## Key Features

*   **User Input**:  Prompts the user for the target token (either ticker symbol or contract address) and the amount of SOL to swap.
*   **Token Resolution**: Tries to resolve the ticker symbol to a token contract address using `TokenDataManager.get_token_address_from_ticker()`.  If the input is not a valid ticker, it is treated as a contract address.
*   **Coingecko Integration (Optional)**: Fetches and displays price data for the target token from CoinGecko, including price, market cap, and 24-hour performance metrics.
*   **User Confirmation**: Asks the user to confirm the trade before execution.
*   **Trade Execution**: Executes the swap using `TradeManager.trade()` via the Jupiter aggregator, if the user confirms.
*   **Error Handling**: Includes basic error handling for invalid user input, ticker resolution failures, and swap failures.
*   **Mainnet Deployment**:  Uses the Solana mainnet RPC endpoint for live trading.

## Files

*   `main.py`: The main script that implements the trade execution flow.
*   `.env.example`:  An example `.env` file to guide the user on setting up the environment.  Contains `SOLANA_PRIVATE_KEY="your_private_key"`.

## How to Run

1.  **Set up your environment**:
    *   Create a virtual environment (recommended) `python -m venv venv`
    *   Activate the virtual environment `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows).
    *   Install AgentiPy: `pip install agentipy`
    *   Create a `.env` file in the same directory as `main.py` and add your Solana private key: `SOLANA_PRIVATE_KEY="your_private_key"`

2.  **Run the script**:  `python main.py`

3.  **Follow the prompts**: The script will ask you for the target token (ticker or contract address) and the amount of SOL you want to swap. It may also show token information.  Confirm the trade when prompted.

## Code Breakdown

1.  **Imports**: Imports necessary modules from AgentiPy and other libraries.
2.  **Environment Variable Loading**: Loads the Solana private key from the `.env` file.
3.  **User Input**:
    *   Prompts the user for the target token and the amount of SOL.
    *   Includes input validation to ensure a positive SOL amount.
4.  **Token Resolution**:
    *   Attempts to interpret user input as either a contract address or a ticker symbol.
    *   Uses `TokenDataManager.get_token_address_from_ticker()` to resolve the ticker.
5.  **Coingecko Data Fetching (Optional)**:
    *   If a valid token address is determined, it fetches token price data from CoinGecko using `CoingeckoManager.get_token_price_data()`.
    *   Displays price, market cap, and other relevant information.
6.  **User Confirmation**:  Asks the user to confirm the swap based on the entered data and optional coingecko data.
7.  **Trade Execution**:
    *   If the user confirms, it calls `TradeManager.trade()` to execute the swap on Jupiter using the provided target token and SOL amount.
    *   Prints the transaction signature if the trade is successful.
    *   Handles potential errors during the swap.
8.  **Error Handling**: Provides basic error messages to the user for various failure scenarios (invalid input, ticker resolution, swap failures).

## Security Considerations

*   **Private Key Security**: The most important security consideration is the handling of your private key.  **Never hardcode your private key directly into your code**, especially for a live application.  Use environment variables (as shown here), secure key vaults, or hardware wallets.
*   **Malicious Tokens**: Be careful when entering a token address.  Verify the token's authenticity and legitimacy before trading.  Trade at your own risk.
*   **Slippage Tolerance**: This example does *not* set a slippage tolerance. In a production environment, always set a reasonable slippage tolerance to protect against price fluctuations during the trade.
*   **RPC Endpoint**:  This example uses the public Solana mainnet RPC endpoint.  For high-volume trading or production applications, consider using a dedicated RPC endpoint provider for better performance and reliability.
