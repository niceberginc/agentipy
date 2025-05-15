"""
Dune Analytics Echo API integration for retrieving lending protocol data.
This module provides functionality to fetch and process lending protocol data using Dune's Echo API.
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from dune_client.client import DuneClient
from dune_client.types import QueryParameter

logger = logging.getLogger(__name__)

class DuneLendingProtocols:
    """
    A class for interacting with Dune Echo API to retrieve lending protocols data
    across multiple chains with real-time performance.
    """
    
    # Echo API endpoints for lending protocols
    LENDING_PROTOCOLS_QUERY = 3509967  # Example ID - replace with actual Echo API query ID
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Dune Lending Protocols client using Echo API.
        
        Args:
            api_key (str, optional): Dune API key. If not provided, will try to load from env.
        """
        self.api_key = api_key or os.environ.get("DUNE_API_KEY")
        if not self.api_key:
            raise ValueError("Dune API key is required. Provide it directly or set DUNE_API_KEY env variable.")
        
        self.client = DuneClient(self.api_key)
    
    def get_lending_protocols(self, chain: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get a list of lending protocols using Echo API for real-time data.
        
        Args:
            chain (str, optional): Filter by specific blockchain (e.g., "ethereum", "arbitrum").
                                 If None, returns data for all supported chains.
        
        Returns:
            List[Dict[str, Any]]: List of lending protocols with their details including:
                - protocol_name: Name of the lending protocol
                - chain: Blockchain where the protocol is deployed
                - total_supplied: Total value supplied to the protocol
                - total_borrowed: Total value borrowed from the protocol
                - supported_assets: List of supported assets
                - contract_addresses: Protocol's contract addresses
        """
        params = []
        if chain:
            params.append(QueryParameter.text_type(name="Chain", value=chain))
            
        try:
            # Using Echo API endpoint for faster response
            results = self.client.get_latest_result(
                query_id=self.LENDING_PROTOCOLS_QUERY,
                max_age_hours=1  # Echo API data is real-time, so we can use a short cache
            )
            
            if chain:
                # Filter results by chain if specified
                return [
                    protocol for protocol in results.get('result', {}).get('rows', [])
                    if protocol.get('chain', '').lower() == chain.lower()
                ]
            return results.get('result', {}).get('rows', [])
            
        except Exception as e:
            logger.error(f"Error fetching lending protocols from Echo API: {e}")
            return []

    def get_protocol_balances(self, protocol_name: str, wallet_address: str) -> Dict[str, Any]:
        """
        Get user balances and positions in a specific lending protocol using Echo API.
        
        Args:
            protocol_name (str): Name of the lending protocol
            wallet_address (str): User's wallet address
            
        Returns:
            Dict[str, Any]: User's positions in the protocol including:
                - supplied_assets: List of supplied assets and amounts
                - borrowed_assets: List of borrowed assets and amounts
                - health_factor: Account health factor if applicable
                - collateral_value: Total collateral value
        """
        try:
            # Echo API call for real-time balance data
            params = [
                QueryParameter.text_type(name="protocol", value=protocol_name),
                QueryParameter.text_type(name="address", value=wallet_address)
            ]
            
            query = self.client.run_query_with_filters(
                query_id=self.LENDING_PROTOCOLS_QUERY,
                filters=f"protocol={protocol_name}&address={wallet_address}"
            )
            
            if not query or 'result' not in query:
                return {}
                
            return query['result']
            
        except Exception as e:
            logger.error(f"Error fetching protocol balances from Echo API: {e}")
            return {}

    def create_custom_query(self, sql: str, name: str, params: List[QueryParameter] = None) -> int:
        """
        Create a custom query on Dune and return its ID.
        Useful for creating new queries for specific lending protocol data needs.
        
        Args:
            sql (str): The SQL query text.
            name (str): Name for the query.
            params (List[QueryParameter], optional): List of query parameters.
            
        Returns:
            int: The ID of the created query
        """
        try:
            query = self.client.create_query(
                name=name,
                query_sql=sql,
                params=params or [],
                is_private=False
            )
            return query.base.query_id
        except Exception as e:
            logger.error(f"Error creating custom query: {e}")
            raise 