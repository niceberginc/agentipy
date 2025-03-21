import aiohttp
from agentipy.agent import SolanaAgentKit


class CoingeckoManager:
    @staticmethod
    async def get_trending_tokens(agent: SolanaAgentKit) -> dict:
        """
        Get trending tokens from CoinGecko (Free endpoint).

        Args:
            agent (SolanaAgentKit): The Solana agent instance.

        Returns:
            dict: Trending tokens data.
        """
        try:
            # Always use the free endpoint for trending tokens
            url = "https://api.coingecko.com/api/v3/search/trending"
            # Optionally add a demo key if provided (and no pro key is set)
            if not agent.coingecko_api_key and agent.coingecko_demo_api_key:
                url += f"?x_cg_demo_api_key={agent.coingecko_demo_api_key}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch trending tokens: {response.status}")
                    data = await response.json()
                    return data
        except Exception as e:
            raise Exception(f"Couldn't get trending tokens: {e}")

    @staticmethod
    async def get_trending_pools(agent: SolanaAgentKit, duration: str = "24h") -> dict:
        """
        Get trending pools from CoinGecko for the Solana network (Pro endpoint).

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            duration (str): Duration filter for trending pools. Allowed values: "5m", "1h", "6h", "24h". Default is "24h".

        Returns:
            dict: Trending pools data.
        """
        try:
            if not agent.coingecko_api_key:
                raise Exception("No CoinGecko Pro API key provided")
            
            url = (
                "https://pro-api.coingecko.com/api/v3/onchain/networks/solana/trending_pools"
                f"?include=base_token,network&duration={duration}"
            )
            headers = {"x-cg-pro-api-key": agent.coingecko_api_key}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch trending pools: {response.status}")
                    data = await response.json()
                    return data
        except Exception as e:
            raise Exception(f"Error fetching trending pools from CoinGecko: {e}")
        
    @staticmethod
    async def get_top_gainers(
        agent: SolanaAgentKit,
        duration: str = "24h",  # Allowed values: "1h", "24h", "7d", "14d", "30d", "60d", "1y"
        top_coins: int | str = "all"  # Allowed values: 300, 500, 1000, or "all"
    ) -> dict:
        """
        Get top gainers from CoinGecko (Pro endpoint).

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            duration (str): Duration filter for top gainers. Default is "24h".
            top_coins (int or str): The number of top coins to return. Default is "all".

        Returns:
            dict: Top gainers data.
        """
        try:
            if not agent.coingecko_api_key:
                raise Exception("No CoinGecko Pro API key provided")
            
            url = (
                "https://pro-api.coingecko.com/api/v3/coins/top_gainers_losers"
                f"?vs_currency=usd&duration={duration}&top_coins={top_coins}"
            )
            headers = {"x-cg-pro-api-key": agent.coingecko_api_key}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch top gainers: {response.status}")
                    data = await response.json()
                    return data
        except Exception as e:
            raise Exception(f"Error fetching top gainers from CoinGecko: {e}")

    @staticmethod
    async def get_token_price_data(agent: SolanaAgentKit, token_addresses: list[str]) -> dict:
        """
        Get token price data for a list of token addresses from CoinGecko (Free endpoint).

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            token_addresses (list[str]): A list of token contract addresses.

        Returns:
            dict: Token price data from CoinGecko.
        """
        try:
            joined_addresses = ",".join(token_addresses)
            url = (
                "https://api.coingecko.com/api/v3/simple/token_price/solana"
                f"?contract_addresses={joined_addresses}"
                "&vs_currencies=usd"
                "&include_market_cap=true"
                "&include_24hr_vol=true"
                "&include_24hr_change=true"
                "&include_last_updated_at=true"
            )
            if not agent.coingecko_api_key and agent.coingecko_demo_api_key:
                url += f"&x_cg_demo_api_key={agent.coingecko_demo_api_key}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch token price data: {response.status}")
                    data = await response.json()
                    return data
        except Exception as e:
            raise Exception(f"Error fetching token price data from CoinGecko: {e}")
        
    @staticmethod
    async def get_token_info(agent: SolanaAgentKit, token_address: str) -> dict:
        """
        Get token info for a given token address from CoinGecko (Pro endpoint).

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            token_address (str): The token's contract address.

        Returns:
            dict: Token info data.
        """
        try:
            if not agent.coingecko_api_key:
                raise Exception("No CoinGecko Pro API key provided")
            
            url = f"https://pro-api.coingecko.com/api/v3/onchain/networks/solana/tokens/{token_address}/info"
            headers = {"x-cg-pro-api-key": agent.coingecko_api_key}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch token info: {response.status}")
                    data = await response.json()
                    return data
        except Exception as e:
            raise Exception(f"Error fetching token info from CoinGecko: {e}")

    @staticmethod
    async def get_latest_pools(agent: SolanaAgentKit) -> dict:
        """
        Get the latest pools from CoinGecko for the Solana network (Pro endpoint).

        Args:
            agent (SolanaAgentKit): The Solana agent instance.

        Returns:
            dict: Latest pools data.
        """
        try:
            if not agent.coingecko_api_key:
                raise Exception("No CoinGecko Pro API key provided")
            
            url = (
                "https://pro-api.coingecko.com/api/v3/onchain/networks/solana/new_pools"
                f"?include=base_token,network"
            )
            headers = {"x-cg-pro-api-key": agent.coingecko_api_key}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch latest pools: {response.status}")
                    data = await response.json()
                    return data
        except Exception as e:
            raise Exception(f"Error fetching latest pools from CoinGecko: {e}")
        
    @staticmethod
    async def get_coin_price_vs(agent: SolanaAgentKit, coin_ids: list[str], vs_currencies: list[str] = ["usd"]) -> dict:
        """
        Get trending tokens from CoinGecko (Free endpoint).

        Args:
            agent (SolanaAgentKit): The Solana agent instance.

        Returns:
            dict: Trending tokens data.
        """
        try:
            joined_addresses = ",".join(coin_ids)
            joined_currencies = ",".join(vs_currencies)
       
            url = (
                "https://api.coingecko.com/api/v3/simple/price"
                f"?ids={joined_addresses}"
                f"&vs_currencies={joined_currencies}"
                "&include_market_cap=true"
                "&include_24hr_vol=true"
                "&include_24hr_change=true"
                "&include_last_updated_at=true")
 

            # Optionally add a demo key if provided (and no pro key is set)
            if not agent.coingecko_api_key and agent.coingecko_demo_api_key:
                url += f"?x_cg_demo_api_key={agent.coingecko_demo_api_key}"              
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch trending tokens: {response.status}")
                    data = await response.json()
                    return data
        except Exception as e:
            raise Exception(f"Couldn't get trending tokens: {e}")
