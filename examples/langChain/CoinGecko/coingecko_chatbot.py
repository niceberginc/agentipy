import asyncio
import json
import time
from agentipy.agent import SolanaAgentKit
from agentipy.langchain.coingecko import get_coingecko_tools

def initialize_solana_kit(api_key):
    return SolanaAgentKit(coingecko_api_key=api_key)

# Load all CoinGecko tools
def load_tools(solana_kit):
    return get_coingecko_tools(solana_kit)

# Export data to a JSON file
def export_data(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data exported to {filename}")

# Chatbot interaction
async def chatbot():
    # Prompt user for CoinGecko API key
    api_key = input("Enter your CoinGecko API key: ").strip()
    solana_kit = initialize_solana_kit(api_key)
    tools = load_tools(solana_kit)

    print("Welcome to the CoinGecko Chatbot! Type 'exit' to quit.")

    while True:
        user_input = input("\nWhat would you like to know? ").strip().lower()

        if user_input == "exit":
            print("Goodbye!")
            break

        # Tool 1: Get Top Gainers
        if "top gainers" in user_input:
            gainers_tool = next(t for t in tools if t.name == "coingecko_get_top_gainers")
            gainers_input = json.dumps({"duration": "1h", "top_coins": 10})
            result = await gainers_tool._arun(gainers_input)
            print(f"🔼 Top Gainers (1h):\n{json.dumps(result, indent=4)}")
            if result.get("top_gainers") is not None:
                export = input("Export this data? (yes/no): ").strip().lower()
                if export == "yes":
                    export_data(result, "top_gainers.json")
            else:
                print("Error: Unable to fetch top gainers. Check your API key or try again later.")

        # Tool 2: Get Latest Pools
        elif "latest pools" in user_input:
            latest_pools_tool = next(t for t in tools if t.name == "coingecko_get_latest_pools")
            result = await latest_pools_tool._arun()
            print(f"💧 Latest Pools:\n{json.dumps(result, indent=4)}")
            if result.get("latest_pools") is not None:
                export = input("Export this data? (yes/no): ").strip().lower()
                if export == "yes":
                    export_data(result, "latest_pools.json")
            else:
                print("Error: Unable to fetch latest pools. Check your API key or try again later.")

        # Tool 3: Get Token Price Data
        elif "token prices" in user_input:
            price_tool = next(t for t in tools if t.name == "coingecko_get_token_price_data")
            token_addresses = input("Enter token addresses (comma-separated): ").strip().split(",")
            price_input = json.dumps({"token_addresses": token_addresses})
            result = await price_tool._arun(price_input)
            print(f"💲 Token Prices:\n{json.dumps(result, indent=4)}")
            if result.get("price_data") is not None:
                export = input("Export this data? (yes/no): ").strip().lower()
                if export == "yes":
                    export_data(result, "token_prices.json")
            else:
                print("Error: Unable to fetch token prices. Check your API key or token addresses.")

        # Tool 4: Get Trending Tokens
        elif "trending tokens" in user_input:
            trending_tokens_tool = next(t for t in tools if t.name == "coingecko_get_trending_tokens")
            result = await trending_tokens_tool._arun()
            print(f"🚀 Trending Tokens:\n{json.dumps(result, indent=4)}")
            if result.get("trending_tokens") is not None:
                export = input("Export this data? (yes/no): ").strip().lower()
                if export == "yes":
                    export_data(result, "trending_tokens.json")
            else:
                print("Error: Unable to fetch trending tokens. Check your API key or try again later.")

        else:
            print("Sorry, I don't understand that command. Try one of these:")
            print("- What are the top gainers?")
            print("- Show me the latest pools.")
            print("- Get token prices.")
            print("- What are the trending tokens?")

        time.sleep(1)

if __name__ == "__main__":
    asyncio.run(chatbot())