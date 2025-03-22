import asyncio
import json
import os
import datetime
from agentipy.agent import SolanaAgentKit
from agentipy.langchain.elfaai import get_elfaai_tools

async def main():
    # Load required environment variables
    private_key = os.getenv("SOLANA_PRIVATE_KEY")
    elfa_ai_api_key = os.getenv("ELFA_AI_API_KEY")
    
    if not private_key or not elfa_ai_api_key:
        print("ERROR: Missing required environment variables!")
        print('Run the following in your terminal:')
        print('export SOLANA_PRIVATE_KEY="your_base58_private_key_here"')
        print('export ELFA_AI_API_KEY="your_elfa_ai_api_key_here"')
        return

    try:
        solana_kit = SolanaAgentKit(private_key=private_key, elfa_ai_api_key=elfa_ai_api_key)
    except Exception as e:
        print("Error initializing SolanaAgentKit:", e)
        return

    # Load tools from Elfa AI
    tools = get_elfaai_tools(solana_kit)

    # Let user select which analysis to run
    print("Choose an analysis option:")
    print("1. Get Smart Mentions")
    print("2. Get Top Mentions by Ticker")
    print("3. Search Mentions by Keywords (with date range)")
    print("4. Get Trending Tokens")
    print("5. Get Twitter Stats")
    choice = input("Enter your choice (1-5): ").strip()

    results = {}

    if choice == "1":
        # Get Smart Mentions
        limit = input("Enter number of smart mentions to retrieve (default 5): ").strip() or "5"
        offset = input("Enter offset (default 0): ").strip() or "0"
        smart_mentions_input = json.dumps({
            "limit": int(limit),
            "offset": int(offset)
        })
        tool = next(tool for tool in tools if tool.name == "elfa_ai_get_smart_mentions")
        results["Smart Mentions"] = await tool._arun(smart_mentions_input)

    elif choice == "2":
        # Get Top Mentions by Ticker
        ticker = input("Enter token ticker (e.g., SOL): ").strip() or "SOL"
        time_window = input("Enter time window (e.g., 1h): ").strip() or "1h"
        page = input("Enter page number (default 1): ").strip() or "1"
        page_size = input("Enter page size (default 5): ").strip() or "5"
        include_details_input = input("Include account details? (yes/no, default no): ").strip().lower()
        # Convert input to Boolean (True if user says yes, else False)
        include_details = True if include_details_input.startswith("y") else False
        top_mentions_input = json.dumps({
            "ticker": ticker,
            "time_window": time_window,
            "page": int(page),
            "page_size": int(page_size),
            "include_account_details": include_details
        })
        tool = next(tool for tool in tools if tool.name == "elfa_ai_get_top_mentions_by_ticker")
        results["Top Mentions by Ticker"] = await tool._arun(top_mentions_input)

    elif choice == "3":
        # Search Mentions by Keywords with a date range
        keywords = input("Enter keywords for search: ").strip()
        from_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
        to_date_str = input("Enter end date (YYYY-MM-DD): ").strip()
        try:
            from_timestamp = int(datetime.datetime.strptime(from_date_str, "%Y-%m-%d").timestamp())
            to_timestamp = int(datetime.datetime.strptime(to_date_str, "%Y-%m-%d").timestamp())
        except Exception as e:
            print("Error parsing dates:", e)
            return

        # Validate date range: must be at least 1 day and at most 30 days
        one_day = 86400
        thirty_days = 30 * one_day
        diff = to_timestamp - from_timestamp
        if diff < one_day or diff > thirty_days:
            print("Error: The date range must be between 1 and 30 days.")
            return

        # Get limit input and enforce allowed range (20-30)
        limit_input = input("Enter number of results to retrieve (default 5): ").strip()
        try:
            requested_limit = int(limit_input) if limit_input else 5
        except ValueError:
            requested_limit = 5

        if requested_limit < 20:
            print("Note: Limit must be between 20 and 30. Using minimum value of 20.")
            requested_limit = 20
        elif requested_limit > 30:
            print("Note: Limit must be between 20 and 30. Using maximum value of 30.")
            requested_limit = 30

        search_mentions_input = json.dumps({
            "keywords": keywords,
            "from_timestamp": from_timestamp,
            "to_timestamp": to_timestamp,
            "limit": requested_limit,
            "cursor": ""
        })
        tool = next(tool for tool in tools if tool.name == "elfa_ai_search_mentions_by_keywords")
        results["Search Mentions by Keywords"] = await tool._arun(search_mentions_input)

    elif choice == "4":
        # Get Trending Tokens
        time_window = input("Enter time window (default 24h): ").strip() or "24h"
        page = input("Enter page number (default 1): ").strip() or "1"
        page_size = input("Enter number of tokens to show (default 10): ").strip() or "10"
        min_mentions = input("Enter minimum mentions (default 5): ").strip() or "5"
        trending_tokens_input = json.dumps({
            "time_window": time_window,
            "page": int(page),
            "page_size": int(page_size),
            "min_mentions": int(min_mentions)
        })
        tool = next(tool for tool in tools if tool.name == "elfa_ai_get_trending_tokens")
        results["Trending Tokens"] = await tool._arun(trending_tokens_input)

    elif choice == "5":
        # Get Twitter Stats
        username = input("Enter Twitter username: ").strip()
        twitter_stats_input = json.dumps({
            "username": username
        })
        tool = next(tool for tool in tools if tool.name == "elfa_ai_get_smart_twitter_account_stats")
        results["Twitter Stats"] = await tool._arun(twitter_stats_input)

    else:
        print("Invalid choice!")
        return

    for name, result in results.items():
        print(f"\n{name}:\n{json.dumps(result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())
