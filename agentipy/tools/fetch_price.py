import aiohttp

from agentipy.helpers import fix_asyncio_for_windows

fix_asyncio_for_windows()

class TokenPriceFetcher:
    @staticmethod
    async def fetch_price(token_id: str) -> str:
        """
        Fetch the price of a given token in USDC using Jupiter API (v3).

        Args:
            token_id (str): The token mint address.

        Returns:
            str: The price of the token in USDC.

        Raises:
            Exception: If the fetch request fails or price data is unavailable.
        """
        #v3
        url = f"https://lite-api.jup.ag/price/v3?ids={token_id}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        if response.status == 400:
                            error_text = await response.text()
                            raise Exception(f"Failed to fetch price (400 Bad Request): {error_text}")
                        elif response.status == 404:
                            error_text = await response.text()
                            raise Exception(f"Failed to fetch price (404 Not Found): {error_text}")
                        else:
                            raise Exception(f"Failed to fetch price: {response.status}")

                    data = await response.json()

                    token_data = data.get(token_id) 
                    if token_data:
                        price = token_data.get("usdPrice") 
                    else:
                        price = None 

                    if price is None: 
                        raise Exception(f"Price data not available for token ID: {token_id}. Response: {data}")

                    return str(price)
        except Exception as e:
            raise Exception(f"Price fetch failed: {str(e)}")