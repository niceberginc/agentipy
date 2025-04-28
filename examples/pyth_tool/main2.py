import asyncio
import os
from dotenv import load_dotenv
from agentipy.tools.use_pyth import PythManager
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import Tool, AgentExecutor, create_openai_tools_agent
from langchain_community.tools import DuckDuckGoSearchRun
from pythclient.pythaccounts import PythPriceAccount, PythPriceStatus
from pythclient.solana import SolanaClient, SolanaPublicKey

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise RuntimeError(
        "Environment variable OPENAI_API_KEY is not set. "
        "Please add it to your .env file or export it in your shell."
    )

os.environ["OPENAI_API_KEY"] = api_key

PYTHNET_ENDPOINT = "https://pythnet.rpcpool.com/"
VALID_FEEDS_URL = "https://pyth.network/developers/price-feed-ids"

PREDEFINED_FEEDS = {
    "sol": ("SOL/USD", "H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG"),
    "btc": ("BTC/USD", "GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU"),
    "eth": ("ETH/USD", "JBu1AL4obBcCMqKBBxhpWCNUt136ijcuMZLFvTP7iWdB"),
}

async def validate_mint_address(mint_address: str) -> bool:
    """Validate Pyth network mint address via on-chain status check."""
    client = SolanaClient(endpoint=PYTHNET_ENDPOINT)
    try:
        account = PythPriceAccount(SolanaPublicKey(mint_address), client)
        await account.update()
        return account.aggregate_price_status == PythPriceStatus.TRADING
    except Exception:
        return False
    finally:
        await client.close()

async def analyze_token():
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7)
    search = DuckDuckGoSearchRun()

    tools = [
        Tool(
            name="MarketSearch",
            func=search.run,
            description="Search for latest cryptocurrency news and market trends"
        )
    ]

    # Agent prompt setup
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Analyze cryptocurrency prices using:
        1. Verified on-chain data from Pyth Network
        2. Latest market developments
        Provide: Technical analysis, risk assessment, and short-term prediction"""),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    token = input("Enter token (btc/sol/eth) or 'custom': ").lower()

    if token == "custom":
        symbol = input("Symbol (e.g. XYZ/USD): ").strip()
        mint_address = input("Pyth mint address: ").strip()

        is_valid = await validate_mint_address(mint_address)
        if not is_valid:
            print(f"Invalid Pyth feed address. Check valid feeds at:\n{VALID_FEEDS_URL}")
            return
    else:
        try:
            symbol, mint_address = PREDEFINED_FEEDS[token]
        except KeyError:
            print(f"Available tokens: {', '.join(PREDEFINED_FEEDS.keys())}")
            return

    print(f"\n🔍 Fetching {symbol} data...")
    try:
        price_data = await PythManager.get_price(mint_address)

        if price_data["status"] != "TRADING":
            raise ValueError(f"Price feed not active: {price_data['status']}")

        analysis = await executor.ainvoke({
            "input": f"""Analyze {symbol} with:
            - Current Price: ${price_data['price']:,.4f}
            - Confidence Interval: ±${price_data['confidence_interval']:,.4f}
            Provide comprehensive market analysis"""
        })

        print(f"\n {symbol} Analysis")
        print(f"• Current Price: ${price_data['price']:,.4f}")
        print(f"• Confidence Range: ±${price_data['confidence_interval']:,.4f}")
        print(f"\n Market Insights:\n{analysis['output']}")

    except Exception as e:
        print(f"\n Analysis failed: {str(e)}")
        web_results = search.run(f"{symbol} cryptocurrency latest news")
        print(f"\n Latest Web Results:\n{web_results[:500]}...")

if __name__ == "__main__":
    asyncio.run(analyze_token())
