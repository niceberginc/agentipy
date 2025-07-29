import asyncio
from agentipy.tools.fetch_price import TokenPriceFetcher

async def main():
    sol_mint = "So11111111111111111111111111111111111111112"
    try:
        sol_price = await TokenPriceFetcher.fetch_price(sol_mint)
        print(f"SOL Price in USDC: {sol_price}")
    except Exception as e:
        print(f"Failed to fetch SOL price: {e}")

    print("-" * 20)

    usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    try:
        usdc_price = await TokenPriceFetcher.fetch_price(usdc_mint)
        print(f"USDC Price in USDC: {usdc_price}") 
    except Exception as e:
        print(f"Failed to fetch USDC price: {e}")

    print("-" * 20)

if __name__ == "__main__":
    asyncio.run(main())