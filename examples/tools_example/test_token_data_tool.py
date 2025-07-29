from agentipy.tools.get_token_data import TokenDataManager
from solders.pubkey import Pubkey

def test_get_token_data(ticker: str):
    try:
        print(f"\n Searching for token: {ticker}")

        # Step 1: Get token address
        address = TokenDataManager.get_token_address_from_ticker(ticker)
        if not address:
            print(f"Could not find address for {ticker}")
            return

        print(f"Found address: {address}")

        # Step 2: Get token data from Jupiter
        pubkey = Pubkey.from_string(address)
        token_data = TokenDataManager.get_token_data_by_address(pubkey)

        if token_data:
            print(f"Token Data:\n"
                  f" - Symbol: {token_data.symbol}\n"
                  f" - Name:   {token_data.name}\n"
                  f" - Address:{token_data.address}")
        else:
            print("No token data found from Jupiter.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # You can test with popular tickers like 'SOL', 'BONK', 'JUP', 'TRUMP' etc.
    test_get_token_data("BONK")
