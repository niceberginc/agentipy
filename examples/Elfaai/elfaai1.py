import asyncio
import json
import os
from agentipy.agent import SolanaAgentKit
from agentipy.langchain.elfaai import get_elfaai_tools

async def main():
    private_key = os.getenv("SOLANA_PRIVATE_KEY")
    elfa_ai_api_key = os.getenv("ELFA_AI_API_KEY")

    if not private_key or not elfa_ai_api_key:
        print("ERROR: Missing required environment variables!")
        print("Run the following in your terminal:")
        print('export SOLANA_PRIVATE_KEY="your_base58_private_key_here"')
        print('export ELFA_AI_API_KEY="your_elfa_ai_api_key_here"')
        return

    try:
        solana_kit = SolanaAgentKit(private_key=private_key, elfa_ai_api_key=elfa_ai_api_key)
    except Exception as e:
        print("Error initializing SolanaAgentKit:", e)
        return

    tools = get_elfaai_tools(solana_kit)
    results = {}

    # Get Smart Mentions
    smart_mentions_tool = next(tool for tool in tools if tool.name == "elfa_ai_get_smart_mentions")
    smart_mentions_input = json.dumps({"limit": 5, "offset": 0}) 
    results["Smart Mentions"] = await smart_mentions_tool._arun(smart_mentions_input)

    # Get Top Mentions by Ticker
    top_mentions_tool = next(tool for tool in tools if tool.name == "elfa_ai_get_top_mentions_by_ticker")
    top_mentions_input = json.dumps({
        "ticker": "SOL",
        "time_window": "1h",
        "page": 1,
        "page_size": 5,
        "include_account_details": True
    })
    results["Top Mentions by Ticker"] = await top_mentions_tool._arun(top_mentions_input)

    # Search Mentions by Keywords
    search_mentions_tool = next(tool for tool in tools if tool.name == "elfa_ai_search_mentions_by_keywords")
    search_mentions_input = json.dumps({
        "keywords": "Solana blockchain", 
        "from_timestamp": 1672531200,  
        "to_timestamp": 1740787200,
        "limit": 5
    })
    results["Search Mentions by Keywords"] = await search_mentions_tool._arun(search_mentions_input)


    # Get Trending Tokens
    trending_tokens_tool = next(tool for tool in tools if tool.name == "elfa_ai_get_trending_tokens")
    trending_tokens_input = json.dumps({
        "time_window": "24h",
        "page": 1,
        "page_size": 10,
        "min_mentions": 5
    })
    results["Trending Tokens"] = await trending_tokens_tool._arun(trending_tokens_input)

    # Get Smart Twitter Account Stats
    twitter_stats_tool = next(tool for tool in tools if tool.name == "elfa_ai_get_smart_twitter_account_stats")
    twitter_stats_input = json.dumps({
        "username": "solana"
    })
    results["Twitter Stats"] = await twitter_stats_tool._arun(twitter_stats_input)

    # Print results
    for name, result in results.items():
        print(f"\n{name}:\n", json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())