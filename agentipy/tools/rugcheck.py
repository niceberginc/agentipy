import logging

import requests

from agentipy.types import TokenCheck

BASE_URL = "https://api.rugcheck.xyz/v1"

logger = logging.getLogger(__name__)

class RugCheckManager:
    @staticmethod

    async def fetch_token_report_summary(mint: str) -> TokenCheck:
        """
        Fetches a summary report for a specific token.
        
        Args:
            mint (str): The mint address of the token.

        Returns:
            TokenCheck: The token summary report.

        Raises:
            Exception: If the API call fails.
        """

        try:
            response = requests.get(f"{BASE_URL}/tokens/{mint}/report/summary")
            response.raise_for_status()
            return TokenCheck(**response.json())
        except requests.RequestException as error:
            logger.info(f"Error fetching report summary for token {mint}: {error}")
            raise Exception(f"Failed to fetch report summary for token {mint}") from error
    
    @staticmethod
    async def fetch_token_detailed_report(mint:str) -> TokenCheck:
        """
        Fetches a detailed report for a specific token.
        
        Args:
            mint (str): The mint address of the token.

        Returns:
            TokenCheck: The detailed token report.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.get(f"{BASE_URL}/tokens/{mint}/report")
            response.raise_for_status()
            return TokenCheck(**response.json())
        except requests.RequestException as error:
            logger.info(f"Error fetching detailed report for token {mint}: {error}")
            raise Exception(f"Failed to fetch detailed report for token {mint}.") from error
        
    @staticmethod
    async def fetch_all_domains(page: int = 1, limit: int = 50, verified: bool = None):
        """
        Fetches all registered domains with optional pagination and filtering.

        Args:
            page (int): The page number for pagination (default is 1).
            limit (int): The number of records per page (default is 50).
            verified (bool, optional): Filter for verified domains.

        Returns:
            list: A list of all registered domains.

        Raises:
            Exception: If the API call fails.
        """
        params = {
            "page": page,
            "limit": limit,
        }
        if verified is not None:
            params["verified"] = str(verified).lower()

        try:
            response = requests.get(f"{BASE_URL}/domains", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.info(f"Error fetching all domains: {error}")
            raise Exception("Failed to fetch all domains") from error

    @staticmethod
    async def fetch_domains_csv(verified: bool = None) -> bytes:
        """
        Fetches all registered domains as a CSV file with an optional filter.

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

        try:
            response = requests.get(f"{BASE_URL}/domains/data.csv", params=params)
            response.raise_for_status()
            return response.content
        except requests.RequestException as error:
            logger.info(f"Error fetching domains CSV: {error}")
            raise Exception("Failed to fetch domains CSV") from error
    
    @staticmethod
    async def lookup_domain(domain_id: str) -> dict:
        """
        Fetches details for a specific domain.

        Args:
            domain_id (str): The ID of the domain.

        Returns:
            dict: The domain details.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.get(f"{BASE_URL}/domains/lookup/{domain_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.info(f"Error looking up domain {domain_id}: {error}")
            raise Exception(f"Failed to fetch domain details for {domain_id}") from error

    @staticmethod
    async def fetch_domain_records(domain_id: str) -> dict:
        """
        Fetches DNS records for a specific domain.

        Args:
            domain_id (str): The ID of the domain.

        Returns:
            dict: The domain records.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.get(f"{BASE_URL}/domains/records/{domain_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.info(f"Error fetching records for domain {domain_id}: {error}")
            raise Exception(f"Failed to fetch domain records for {domain_id}") from error

    @staticmethod
    async def fetch_leaderboard() -> list:
        """
        Fetches the leaderboard ranking.

        Returns:
            list: A list of ranked tokens.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.get(f"{BASE_URL}/leaderboard")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.info(f"Error fetching leaderboard: {error}")
            raise Exception("Failed to fetch leaderboard") from error

    @staticmethod
    async def fetch_new_tokens() -> list:
        """
        Fetches recently detected tokens.

        Returns:
            list: A list of recently detected tokens.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.get(f"{BASE_URL}/stats/new_tokens")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.info(f"Error fetching new tokens: {error}")
            raise Exception("Failed to fetch new tokens") from error

    @staticmethod
    async def fetch_most_viewed_tokens() -> list:
        """
        Fetches the most viewed tokens in the last 24 hours.

        Returns:
            list: A list of the most viewed tokens.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.get(f"{BASE_URL}/stats/recent")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.info(f"Error fetching most viewed tokens: {error}")
            raise Exception("Failed to fetch most viewed tokens") from error

    @staticmethod
    async def fetch_trending_tokens() -> list:
        """
        Fetches the most voted-for tokens in the last 24 hours.

        Returns:
            list: A list of the most trending tokens.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.get(f"{BASE_URL}/stats/trending")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.info(f"Error fetching trending tokens: {error}")
            raise Exception("Failed to fetch trending tokens") from error

    @staticmethod
    async def fetch_recently_verified_tokens() -> list:
        """
        Fetches recently verified tokens.

        Returns:
            list: A list of recently verified tokens.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.get(f"{BASE_URL}/stats/trending")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.info(f"Error fetching recently verified tokens: {error}")
            raise Exception("Failed to fetch recently verified tokens") from error
    
    @staticmethod
    async def fetch_token_lp_lockers(token_id: str) -> dict:
        """
        Fetches the LP lockers for a specific token.

        Args:
            token_id (str): The ID of the token.

        Returns:
            dict: The LP lockers for the token.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.get(f"{BASE_URL}/tokens/{token_id}/lockers")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.info(f"Error fetching LP lockers for token {token_id}: {error}")
            raise Exception(f"Failed to fetch LP lockers for token {token_id}") from error

    @staticmethod
    async def fetch_token_flux_lp_lockers(token_id: str) -> dict:
        """
        Fetches the LP lockers from Flux Locker for a specific token.

        Args:
            token_id (str): The ID of the token.

        Returns:
            dict: The LP lockers from Flux Locker.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.get(f"{BASE_URL}/tokens/{token_id}/lockers/flux")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.info(f"Error fetching Flux LP lockers for token {token_id}: {error}")
            raise Exception(f"Failed to fetch Flux LP lockers for token {token_id}") from error

    @staticmethod
    async def fetch_token_votes(mint: str) -> dict:
        """
        Fetches the votes for a specific token.

        Args:
            mint (str): The mint address of the token.

        Returns:
            dict: The token votes.

        Raises:
            Exception: If the API call fails.
        """
        try:
            response = requests.get(f"{BASE_URL}/tokens/{mint}/votes")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.info(f"Error fetching votes for token {mint}: {error}")
            raise Exception(f"Failed to fetch votes for token {mint}") from error

