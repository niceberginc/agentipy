import asyncio
from agentipy.tools.rugcheck import RugCheckManager

async def main():
    api_key = "YOUR_API_KEY"  # Replace with your actual RugCheck API key
    rugcheck = RugCheckManager(api_key)

    print("Enter the Contract Address (CA) of the token.")
    print("Example CA: So11111111111111111111111111111111111111112 (Wrapped SOL)")
    user_input = input("Your input: ").strip()

    try:
        print("\nFetching RugCheck report...\n")
        
        report = await rugcheck.fetch_token_report_summary(user_input)
        print(report.to_user_friendly_string())

        lockers = await rugcheck.fetch_token_lp_lockers(user_input)
        print("\n" + lockers.to_user_friendly_string())

    except Exception as e:
        print(f"\nError: {e}")
        print("Please ensure you entered a valid Contract Address (CA).")
        print("Example CA: So11111111111111111111111111111111111111112 (Wrapped SOL)")

if __name__ == "__main__":
    asyncio.run(main())