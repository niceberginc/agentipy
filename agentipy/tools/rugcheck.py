import logging
from typing import Dict, List, Optional

import aiohttp

from agentipy.types import RiskItem, TokenCheck, TokenLockers, TrendingToken

BASE_URL = "https://api.rugcheck.xyz/v1"

logger = logging.getLogger(__name__)

class RugCheckManager:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json"
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    async def _make_request(self, method: str, url: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict:
        """
        Internal helper function to make API requests, handling potential errors and API key usage.
        """
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                if method == "GET":
                    async with session.get(url, params=params) as response:
                        response.raise_for_status()
                        return await response.json()
                elif method == "POST":
                    async with session.post(url, json=data, params=params) as response:
                        response.raise_for_status()
                        return await response.json()
                elif method == "GET_BYTES":  
                    async with session.get(url, params=params) as response:
                        response.raise_for_status()
                        return await response.read()

                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
        except aiohttp.ClientResponseError as e:
            logger.error(f"HTTP error {e.status}: {e.message} - URL: {url} - Params: {params}")
            raise
        except Exception as e:
            logger.error(f"Error making request to {url}: {str(e)} - Params: {params}")
            raise

    async def fetch_token_report_summary(self, mint: str) -> TokenCheck:
        """
        Fetch a summary report for a token.

        Args:
            mint (str): The mint address of the token.
        
        Returns:
            TokenCheck: The token report data.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/tokens/{mint}/report/summary"
        try:
            data = await self._make_request("GET", url)

            data["risks"] = [RiskItem(**r) for r in data.get("risks", [])]

            return TokenCheck(**data)
        except Exception as e:
            logger.error(f"Error fetching token report: {str(e)}")
            raise


    async def fetch_token_detailed_report(self, mint: str) -> TokenCheck:
        """
        Fetch a detailed report for a token.

        Args:
            mint (str): The mint address of the token.
        
        Returns:
            TokenCheck: The detailed token report.
        
        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/tokens/{mint}/report"
        try:
            data = await self._make_request("GET", url)
            return TokenCheck(**data)
        except Exception as e:
            logger.error(f"Error fetching detailed token report: {str(e)}")
            raise

    async def fetch_all_domains(self, page: int = 1, limit: int = 50, verified: bool = None) -> List[Dict]:
        """
        Fetch all registered domains with optional pagination and filtering.

        Args:
            page (int): The page number for pagination (default is 1).
            limit (int): The number of records per page (default is 50).
            verified (bool, optional): Filter for verified domains.
        
        Returns:
            List[Dict]: A list of all registered domains.

        Raises:
            Exception: If the API call fails.
        """
        params = {
            "page": page,
            "limit": limit,
        }
        if verified is not None:
            params["verified"] = str(verified).lower()

        url = f"{BASE_URL}/domains"
        try:
            data = await self._make_request("GET", url, params=params)
            return data
        except Exception as e:
            logger.error(f"Error fetching all domains: {str(e)}")
            raise

    async def fetch_domains_csv(self, verified: bool = None) -> bytes:
        """
        Fetch all registered domains as a CSV file with an optional filter.

        Args:
            verified (bool, optional): Filter for verified domains.
        
        Returns:
            bytes: CSV file content.
        
        Raises:
            Exception: If the API call fails.
        """
        params = {}
        if verified is not None:
            params["verified"] = str(verified).lower()
        url = f"{BASE_URL}/domains/data.csv"
        try:
            data = await self._make_request("GET_BYTES", url, params=params)
            return data
        except Exception as e:
            logger.error(f"Error fetching domains CSV: {str(e)}")
            raise

    async def lookup_domain(self, domain_id: str) -> Dict:
        """
        Fetch details for a specific domain.

        Args:
            domain_id (str): The ID of the domain.
        
        Returns:
            Dict: The domain details.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/domains/lookup/{domain_id}"
        try:
            data = await self._make_request("GET", url)
            return data
        except Exception as e:
            logger.error(f"Error looking up domain {domain_id}: {str(e)}")
            raise

    async def fetch_domain_records(self, domain_id: str) -> Dict:
        """
        Fetch DNS records for a specific domain.

        Args:
            domain_id (str): The ID of the domain.
        
        Returns:
            Dict: The domain records.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/domains/records/{domain_id}"
        try:
            data = await self._make_request("GET", url)
            return data
        except Exception as e:
            logger.error(f"Error fetching records for domain {domain_id}: {str(e)}")
            raise

    async def fetch_leaderboard(self) -> List[Dict]:
        """
        Fetch the leaderboard ranking.

        Returns:
            List[Dict]: A list of ranked tokens.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/leaderboard"
        try:
            data = await self._make_request("GET", url)
            return data
        except Exception as e:
            logger.error(f"Error fetching leaderboard: {str(e)}")
            raise

    async def fetch_new_tokens(self) -> List[Dict]:
        """
        Fetch recently detected tokens.

        Returns:
            List[Dict]: A list of recently detected tokens.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/stats/new_tokens"
        try:
            data = await self._make_request("GET", url)
            return data
        except Exception as e:
            logger.error(f"Error fetching new tokens: {str(e)}")
            raise

    async def fetch_most_viewed_tokens(self) -> List[Dict]:
        """
        Fetch the most viewed tokens in the last 24 hours.

        Returns:
            List[Dict]: A list of the most viewed tokens.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/stats/recent"
        try:
            data = await self._make_request("GET", url)
            return data
        except Exception as e:
            logger.error(f"Error fetching most viewed tokens: {str(e)}")
            raise

    async def fetch_trending_tokens(self) -> List[TrendingToken]:
        """
        Fetch the most voted-for tokens in the last 24 hours.

        Returns:
            List[TrendingToken]: A list of the most trending tokens.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/stats/trending"
        try:
            data = await self._make_request("GET", url)
            return [TrendingToken(**token) for token in data]
        except Exception as e:
            logger.error(f"Error fetching trending tokens: {str(e)}")
            raise

    async def fetch_recently_verified_tokens(self) -> List[TrendingToken]:
        """
        Fetch recently verified tokens.

        Returns:
            List[TrendingToken]: A list of recently verified tokens.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/stats/recently_verified"
        try:
            data = await self._make_request("GET", url)
            return [TrendingToken(**token) for token in data]
        except Exception as e:
            logger.error(f"Error fetching recently verified tokens: {str(e)}")
            raise

    async def fetch_token_lp_lockers(self, token_id: str) -> TokenLockers:
        """
        Fetch LP lockers for a token.

        Args:
            token_id (str): The ID of the token.
        
        Returns:
            TokenLockers: The LP locker data.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/tokens/{token_id}/lockers"
        try:
            data = await self._make_request("GET", url)
            return TokenLockers(**data)
        except Exception as e:
            logger.error(f"Error fetching LP lockers: {str(e)}")
            raise

    async def fetch_token_flux_lp_lockers(self, token_id: str) -> TokenLockers:
        """
        Fetch Flux LP lockers for a token.

        Args:
            token_id (str): The ID of the token.
        
        Returns:
            TokenLockers: The Flux LP locker data.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/tokens/{token_id}/lockers/flux"
        try:
            data = await self._make_request("GET", url)
            return TokenLockers(**data)
        except Exception as e:
            logger.error(f"Error fetching Flux LP lockers: {str(e)}")
            raise

    async def fetch_token_votes(self, mint: str) -> Dict:
        """
        Fetch the votes for a specific token.

        Args:
            mint (str): The mint address of the token.
        
        Returns:
            Dict: The token votes.

        Raises:
            Exception: If the API call fails.
        """
        url = f"{BASE_URL}/tokens/{mint}/votes"
        try:
            data = await self._make_request("GET", url)
            return data
        except Exception as e:
            logger.error(f"Error fetching votes for token {mint}: {str(e)}")
            raise

            