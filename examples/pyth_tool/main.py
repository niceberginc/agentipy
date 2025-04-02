import asyncio
from agentipy.tools.use_pyth import PythManager

PYTH_FEEDS = {
    "SOL/USD": "H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG",
    "BTC/USD": "GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU",
    "ETH/USD": "JBu1AL4obBcCMqKBBxhpWCNUt136ijcuMZLFvTP7iWdB",
    "TRUMP/USD": "A8G6XyA6fSrsavG63ssAGU3Hnt2oDZARxefREzAY5axH",
}

async def fetch_price(symbol: str, mint_address: str):
    """Fetch and display price for a single symbol"""
    try:
        print(f"\n Fetching {symbol} price...")
        result = await PythManager.get_price(mint_address)
        
        if result["status"] == "TRADING":
            print(f" {symbol}:")
            print(f"   Price: ${result['price']:.4f}")
            print(f"   Confidence: ±${result['confidence_interval']:.4f}")
        else:
            print(f" {symbol} status: {result['status']}")
            print(f"   Reason: {result['message']}")
            
    except ValueError as e:
        print(f"Invalid mint address for {symbol}: {str(e)}")
    except Exception as e:
        print(f"Unexpected error fetching {symbol}: {str(e)}")

async def main():
    """Main async function to fetch prices concurrently"""
    tasks = []
    
    for symbol, address in PYTH_FEEDS.items():
        tasks.append(fetch_price(symbol, address))
    
    await asyncio.gather(*tasks)
    
    print("\n Individual fetch demonstration:")
    await fetch_price("SOL/USD", PYTH_FEEDS["SOL/USD"])

if __name__ == "__main__":
    asyncio.run(main())