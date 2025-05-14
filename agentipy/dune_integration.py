"""
Dune Analytics integration for retrieving lending protocol data.
This module provides functionality to fetch and process lending protocol data from Dune Analytics.
"""

import os
import json
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime, timedelta

from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase

logger = logging.getLogger(__name__)

class DuneLendingProtocols:
    """
    A class for interacting with Dune Analytics to retrieve lending protocols data
    across multiple chains.
    """
    
    # Query IDs for different types of lending protocol data
    # These would need to be updated with actual query IDs from Dune
    LENDING_PROTOCOLS_OVERVIEW_QUERY_ID = 3456701  # Example ID - replace with actual
    LENDING_PROTOCOLS_TVL_QUERY_ID = 3456702  # Example ID - replace with actual
    LENDING_PROTOCOLS_RATES_QUERY_ID = 3456703  # Example ID - replace with actual
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Dune Lending Protocols client.
        
        Args:
            api_key (str, optional): Dune API key. If not provided, will try to load from env.
        """
        self.api_key = api_key or os.environ.get("DUNE_API_KEY")
        if not self.api_key:
            raise ValueError("Dune API key is required. Provide it directly or set DUNE_API_KEY env variable.")
        
        self.client = DuneClient(self.api_key)
        
    def get_lending_protocols(self, chain: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get a list of lending protocols available on Dune.
        
        Args:
            chain (str, optional): Filter by specific blockchain (e.g., "ethereum", "solana").
                                   If None, returns data for all chains.
        
        Returns:
            List[Dict[str, Any]]: List of lending protocols with their details
        """
        params = []
        if chain:
            params.append(QueryParameter.text_type(name="Chain", value=chain))
            
        query = QueryBase(
            name="Lending Protocols Overview",
            query_id=self.LENDING_PROTOCOLS_OVERVIEW_QUERY_ID,
            params=params
        )
        
        try:
            results = self.client.run_query(query)
            return results.get('result', {}).get('rows', [])
        except Exception as e:
            logger.error(f"Error fetching lending protocols: {e}")
            return []
    
    def get_lending_protocol_tvl(self, protocol_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get Total Value Locked (TVL) data for lending protocols.
        
        Args:
            protocol_name (str, optional): Filter by specific protocol name.
                                          If None, returns data for all protocols.
        
        Returns:
            List[Dict[str, Any]]: TVL data for lending protocols
        """
        params = []
        if protocol_name:
            params.append(QueryParameter.text_type(name="ProtocolName", value=protocol_name))
            
        query = QueryBase(
            name="Lending Protocols TVL",
            query_id=self.LENDING_PROTOCOLS_TVL_QUERY_ID,
            params=params
        )
        
        try:
            results = self.client.run_query(query)
            return results.get('result', {}).get('rows', [])
        except Exception as e:
            logger.error(f"Error fetching lending protocols TVL: {e}")
            return []
    
    def get_lending_rates(self, protocol_name: Optional[str] = None, asset: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get current lending and borrowing rates for protocols.
        
        Args:
            protocol_name (str, optional): Filter by specific protocol name.
            asset (str, optional): Filter by specific asset (e.g., "USDC", "ETH").
        
        Returns:
            List[Dict[str, Any]]: Current rates data for lending protocols
        """
        params = []
        if protocol_name:
            params.append(QueryParameter.text_type(name="ProtocolName", value=protocol_name))
        if asset:
            params.append(QueryParameter.text_type(name="Asset", value=asset))
            
        query = QueryBase(
            name="Lending Protocols Rates",
            query_id=self.LENDING_PROTOCOLS_RATES_QUERY_ID,
            params=params
        )
        
        try:
            results = self.client.run_query(query)
            return results.get('result', {}).get('rows', [])
        except Exception as e:
            logger.error(f"Error fetching lending rates: {e}")
            return []
    
    def get_latest_result_cached(self, query_id: int, max_age_hours: int = 24) -> Dict[str, Any]:
        """
        Get the latest result from a query without using execution credits if it's recent enough.
        
        Args:
            query_id (int): The query ID to get results for.
            max_age_hours (int): Maximum age of the results in hours.
        
        Returns:
            Dict[str, Any]: The query results
        """
        try:
            return self.client.get_latest_result(query_id, max_age_hours=max_age_hours)
        except Exception as e:
            logger.error(f"Error fetching latest results for query {query_id}: {e}")
            return {}

    @classmethod
    def create_custom_query(cls, client: DuneClient, sql: str, name: str, params: List[QueryParameter] = None) -> int:
        """
        Create a custom query on Dune and return its ID.
        Useful for creating new queries for specific lending protocol data needs.
        
        Args:
            client (DuneClient): The Dune client instance.
            sql (str): The SQL query text.
            name (str): Name for the query.
            params (List[QueryParameter], optional): List of query parameters.
            
        Returns:
            int: The ID of the created query
        """
        try:
            query = client.create_query(
                name=name,
                query_sql=sql,
                params=params or [],
                is_private=False
            )
            return query.base.query_id
        except Exception as e:
            logger.error(f"Error creating custom query: {e}")
            raise 