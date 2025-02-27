import aiohttp

from agentipy.agent import SolanaAgentKit
from agentipy.constants import ELFA_AI_BASE_URL
from agentipy.utils.elfa_ai import get_headers as get_elfa_ai_headers


class ElfaAiManager:
    BASE_URL = ELFA_AI_BASE_URL

    @staticmethod
    async def ping_elfa_ai_api(agent: SolanaAgentKit) -> dict:
        """
        Ping the Elfa AI API.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.

        Returns:
            dict: API response.
        """
        async with aiohttp.ClientSession(headers=get_elfa_ai_headers(agent)) as session:
            async with session.get(f"{ElfaAiManager.BASE_URL}/v1/ping") as response:
                return await response.json()

    @staticmethod
    async def get_elfa_ai_api_key_status(agent: SolanaAgentKit) -> dict:
        """
        Get the status of the Elfa AI API key.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.

        Returns:
            dict: API key status response.
        """
        async with aiohttp.ClientSession(headers=get_elfa_ai_headers(agent)) as session:
            async with session.get(f"{ElfaAiManager.BASE_URL}/v1/key-status") as response:
                return await response.json()

    @staticmethod
    async def get_smart_mentions(agent: SolanaAgentKit, limit: int = 100, offset: int = 0) -> dict:
        """
        Get smart mentions from Elfa AI.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            limit (int): Number of mentions to retrieve.
            offset (int): Offset for pagination.

        Returns:
            dict: Mentions data.
        """
        params = {"limit": limit, "offset": offset}
        async with aiohttp.ClientSession(headers=get_elfa_ai_headers(agent)) as session:
            async with session.get(f"{ElfaAiManager.BASE_URL}/v1/mentions", params=params) as response:
                return await response.json()

    @staticmethod
    async def get_top_mentions_by_ticker(
        agent: SolanaAgentKit,
        ticker: str,
        time_window: str = "1h",
        page: int = 1,
        page_size: int = 10,
        include_account_details: bool = False
    ) -> dict:
        """
        Get top mentions by ticker.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            ticker (str): The ticker symbol.
            time_window (str): The time window for mentions.
            page (int): Page number.
            page_size (int): Number of results per page.
            include_account_details (bool): Whether to include account details.

        Returns:
            dict: Mentions data.
        """
        params = {
            "ticker": ticker,
            "timeWindow": time_window,
            "page": page,
            "pageSize": page_size,
            "includeAccountDetails": include_account_details
        }
        async with aiohttp.ClientSession(headers=get_elfa_ai_headers(agent)) as session:
            async with session.get(f"{ElfaAiManager.BASE_URL}/v1/top-mentions", params=params) as response:
                return await response.json()

    @staticmethod
    async def search_mentions_by_keywords(
        agent: SolanaAgentKit,
        keywords: str,
        from_timestamp: int,
        to_timestamp: int,
        limit: int = 20,
        cursor: str = None
    ) -> dict:
        """
        Search mentions by keywords.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            keywords (str): Keywords for search.
            from_timestamp (int): Start timestamp.
            to_timestamp (int): End timestamp.
            limit (int): Number of results to fetch.
            cursor (str): Optional cursor for pagination.

        Returns:
            dict: Search results.
        """
        params = {
            "keywords": keywords,
            "from": from_timestamp,
            "to": to_timestamp,
            "limit": limit,
            "cursor": cursor
        }
        async with aiohttp.ClientSession(headers=get_elfa_ai_headers(agent)) as session:
            async with session.get(f"{ElfaAiManager.BASE_URL}/v1/mentions/search", params=params) as response:
                return await response.json()

    @staticmethod
    async def get_trending_tokens_using_elfa_ai(
        agent: SolanaAgentKit,
        time_window: str = "24h",
        page: int = 1,
        page_size: int = 50,
        min_mentions: int = 5
    ) -> dict:
        """
        Get trending tokens using Elfa AI.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            time_window (str): Time window for trending tokens.
            page (int): Page number.
            page_size (int): Number of results per page.
            min_mentions (int): Minimum number of mentions required.

        Returns:
            dict: Trending tokens data.
        """
        params = {
            "timeWindow": time_window,
            "page": page,
            "pageSize": page_size,
            "minMentions": min_mentions
        }
        async with aiohttp.ClientSession(headers=get_elfa_ai_headers(agent)) as session:
            async with session.get(f"{ElfaAiManager.BASE_URL}/v1/trending-tokens", params=params) as response:
                return await response.json()

    @staticmethod
    async def get_smart_twitter_account_stats(agent: SolanaAgentKit, username: str) -> dict:
        """
        Get smart Twitter account statistics.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            username (str): The Twitter username.

        Returns:
            dict: Account statistics data.
        """
        params = {"username": username}
        async with aiohttp.ClientSession(headers=get_elfa_ai_headers(agent)) as session:
            async with session.get(f"{ElfaAiManager.BASE_URL}/v1/account/smart-stats", params=params) as response:
                return await response.json()
