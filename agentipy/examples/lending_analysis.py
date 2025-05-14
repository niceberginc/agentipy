"""
Example script for using the Dune Analytics integration to analyze lending protocols.
This script demonstrates how to fetch and analyze lending protocol data from Dune.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from typing import Dict, List, Any

from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase

from agentipy.dune_integration import DuneLendingProtocols
from agentipy.dune_queries.lending_protocols import (
    BEST_LENDING_OPPORTUNITIES_SQL,
    TOP_LENDING_PROTOCOLS_SQL,
    LENDING_PROTOCOLS_OVERVIEW_SQL
)

# Load environment variables from .env file
load_dotenv()

def example_get_lending_protocols():
    """
    Example of how to get a list of lending protocols from Dune.
    """
    # Initialize the DuneLendingProtocols client
    dune_lending = DuneLendingProtocols()
    
    # Get all lending protocols
    protocols = dune_lending.get_lending_protocols()
    print(f"Found {len(protocols)} lending protocols")
    
    # Get lending protocols on Ethereum only
    eth_protocols = dune_lending.get_lending_protocols(chain="ethereum")
    print(f"Found {len(eth_protocols)} lending protocols on Ethereum")
    
    return protocols

def example_create_custom_query():
    """
    Example of how to create a custom query for lending protocols.
    """
    # Initialize the Dune client
    api_key = os.environ.get("DUNE_API_KEY")
    client = DuneClient(api_key)
    
    # Create a custom query for finding the best lending opportunities
    query_id = DuneLendingProtocols.create_custom_query(
        client=client,
        sql=BEST_LENDING_OPPORTUNITIES_SQL,
        name="Best Lending Opportunities",
        params=[
            QueryParameter.number_type(name="MinTVL", value=1000000)  # Minimum TVL of $1M
        ]
    )
    
    print(f"Created custom query with ID: {query_id}")
    
    # Run the query and get results
    query = QueryBase(
        name="Best Lending Opportunities",
        query_id=query_id,
        params=[
            QueryParameter.number_type(name="MinTVL", value=1000000)
        ]
    )
    
    results = client.run_query(query)
    
    # Convert results to DataFrame for easier analysis
    df = pd.DataFrame(results.get('result', {}).get('rows', []))
    
    # Print top 5 opportunities with highest APY
    print("\nTop 5 Lending Opportunities:")
    if not df.empty:
        top_opportunities = df.head(5)
        for _, row in top_opportunities.iterrows():
            print(f"{row['protocol_name']} on {row['chain']}: {row['asset_symbol']} at {row['supply_rate_apy']:.2f}% APY")
    
    return df

def example_get_top_lending_protocols():
    """
    Example of how to get top lending protocols by volume.
    """
    # Initialize the Dune client
    api_key = os.environ.get("DUNE_API_KEY")
    client = DuneClient(api_key)
    
    # Create a query for top lending protocols
    query_id = DuneLendingProtocols.create_custom_query(
        client=client,
        sql=TOP_LENDING_PROTOCOLS_SQL,
        name="Top Lending Protocols by Volume"
    )
    
    # Run the query
    query = QueryBase(
        name="Top Lending Protocols by Volume",
        query_id=query_id
    )
    
    results = client.run_query(query)
    
    # Convert to DataFrame
    df = pd.DataFrame(results.get('result', {}).get('rows', []))
    
    # Print top protocols
    print("\nTop Lending Protocols by Volume (Last 7 Days):")
    if not df.empty:
        for _, row in df.head(10).iterrows():
            volume_in_millions = row['total_volume_usd'] / 1_000_000
            print(f"{row['protocol_name']} on {row['chain']}: ${volume_in_millions:.2f}M volume, {row['unique_users']} users")
    
    return df

def compare_lending_rates(protocols: List[Dict[str, Any]], asset: str = "USDC"):
    """
    Compare lending rates across different protocols for a specific asset.
    
    Args:
        protocols (List[Dict[str, Any]]): List of protocols to compare
        asset (str): Asset symbol to compare rates for
    """
    # Initialize the DuneLendingProtocols client
    dune_lending = DuneLendingProtocols()
    
    # Get lending rates for the specified asset
    rates = dune_lending.get_lending_rates(asset=asset)
    
    print(f"\nLending Rates Comparison for {asset}:")
    
    if rates:
        # Convert to DataFrame
        df = pd.DataFrame(rates)
        
        # Sort by supply rate (descending)
        df_sorted = df.sort_values(by='supply_rate_apy', ascending=False)
        
        for _, row in df_sorted.head(10).iterrows():
            print(f"{row['protocol_name']} on {row['chain']}: {row['supply_rate_apy']:.2f}% supply, {row['borrow_rate_apy']:.2f}% borrow")
    else:
        print(f"No data found for {asset}")

if __name__ == "__main__":
    # Get list of lending protocols
    protocols = example_get_lending_protocols()
    
    # Get best lending opportunities
    opportunities = example_create_custom_query()
    
    # Get top lending protocols by volume
    top_protocols = example_get_top_lending_protocols()
    
    # Compare lending rates for USDC
    if protocols:
        compare_lending_rates(protocols, asset="USDC")
        
    print("\nExamples completed. To use in your own application, import the DuneLendingProtocols class.") 