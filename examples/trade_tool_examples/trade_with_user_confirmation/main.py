import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.trade import TradeManager
from agentipy.tools.use_coingecko import CoingeckoManager
from agentipy.tools.get_token_data import TokenDataManager
from solders.pubkey import Pubkey
import os
from dotenv import load_dotenv

async def main():
    """
    Simple Trade Execution with User Confirmation:
    1. Prompts the user for a target token (ticker or address) and SOL amount.
    2. Optionally displays Coingecko price data.
    3. Confirms the swap with the user.
    4. Executes the trade using TradeManager.
    """
    # --- Load Environment Variables ---
    load_dotenv() 

    # --- Get Private Key from .env ---
    PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY")
    if not PRIVATE_KEY:
        raise ValueError("SOLANA_PRIVATE_KEY environment variable not set.  Make sure to set it in .env!")

    # Mainnet Token Mint Addresses (SOL is our input - what we're trading away)
    SOL_MINT = Pubkey.from_string("So11111111111111111111111111111111111111112") 

    # -------------------------------------------------------------
    # 1. Get User Input
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
        return  

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
                    target_token_symbol = target_token_input.upper()
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
        agent = SolanaAgentKit(
            private_key=PRIVATE_KEY,
            rpc_url="https://api.mainnet-beta.solana.com"  
        )
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
                # 3. Confirm Swap with User
                # -------------------------------------------------------------
                display_symbol = target_token_symbol if target_token_symbol else target_token_input.upper()
                confirmation = input(f"\nConfirm swap of {swap_amount_sol} SOL for {display_symbol} ({target_token_address})? (yes/no): ").lower()
                if confirmation == "yes":
                    # -------------------------------------------------------------
                    # 4. Execute the Trade
                    # -------------------------------------------------------------
                    try:
                        print(f"Attempting to swap {swap_amount_sol} SOL for {display_symbol} on Jupiter...")
                        transaction_signature = await TradeManager.trade(
                            agent=agent,
                            output_mint=Pubkey.from_string(target_token_address),  # Target token
                            input_amount=swap_amount_sol,        # SOL amount to swap
                            input_mint=SOL_MINT  # We're using SOL as input
                        )
                        print(f"Swap successful!")
                        print(f"Transaction Signature: https://explorer.solana.com/tx/{transaction_signature}")
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
    # Load PRIVATE_KEY from .env file
    load_dotenv()

    # --- Get Private Key from .env ---
    PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY")
    if not PRIVATE_KEY:
        print("Error: SOLANA_PRIVATE_KEY not found in .env file. Please create a .env file and add your key.")
        exit(1) 

    asyncio.run(main())

    