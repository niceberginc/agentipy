import json
import asyncio
import openai
import re
from typing import TypedDict, List, Dict, Optional, Annotated
from langgraph.graph import StateGraph
from agentipy.agent import SolanaAgentKit
from agentipy.langchain.coingecko import get_coingecko_tools

# Set your OpenAI API key here or via environment variable
openai.api_key = ""

class AgentState(TypedDict):
    memory: Annotated[List[str], "multi"]
    trending_tokens: Optional[Dict]
    price_data: Optional[Dict]
    token_info: Optional[Dict]
    top_gainers: Optional[Dict]
    token_analysis: Optional[str]

solana_kit = SolanaAgentKit(
    private_key="",  # Use your private key
    rpc_url="https://api.mainnet-beta.solana.com"
)
tools = get_coingecko_tools(solana_kit)

def extract_trending_list(trending_tokens):
    """
    Helper to extract a list of tokens from trending_tokens.
    If trending_tokens is a dict with a 'coins' key, return that list;
    otherwise, assume trending_tokens is already a list.
    """
    if isinstance(trending_tokens, dict):
        return trending_tokens.get("coins", [])
    return trending_tokens

def is_valid_solana_address(addr: str) -> bool:
    """
    Simple heuristic: Solana addresses are Base58 strings typically 32-44 characters long.
    """
    if not (32 <= len(addr) <= 44):
        return False
    valid_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return all(c in valid_chars for c in addr)

async def fetch_trending_tokens(state: AgentState) -> AgentState:
    """Node: Fetch trending tokens"""
    tool = next(t for t in tools if t.name == "coingecko_get_trending_tokens")
    result = await tool._arun()
    
    state['memory'].append("Fetched trending tokens")
    state['trending_tokens'] = result['trending_tokens']
    return state

async def fetch_price_data(state: AgentState) -> AgentState:
    """Node: Fetch price data for trending tokens"""
    if not state['trending_tokens']:
        return state

    trending_list = extract_trending_list(state['trending_tokens'])
    if not trending_list:
        state['memory'].append("No tokens available for price data")
        return state

    tool = next(t for t in tools if t.name == "coingecko_get_token_price_data")
    addresses = [token["item"]["id"] for token in trending_list[:5]]
    input_json = json.dumps({"token_addresses": addresses})
    
    result = await tool._arun(input_json)
    state['memory'].append(f"Fetched price data for {len(addresses)} tokens")
    state['price_data'] = result['price_data']
    return state

async def fetch_token_info(state: AgentState) -> AgentState:
    """Node: Fetch info for first token"""
    if state['trending_tokens']:
        trending_list = extract_trending_list(state['trending_tokens'])
        if trending_list:
            token_item = trending_list[0]["item"]
            address = token_item.get("contract_address") or token_item.get("id")
            if not is_valid_solana_address(address):
                state['memory'].append(f"Token address '{address}' is not a valid Solana address. Using token item data instead.")
                state['token_info'] = token_item
                return state
            tool = next(t for t in tools if t.name == "coingecko_get_token_info")
            result = await tool._arun(json.dumps({"token_address": address}))
            state['memory'].append(f"Fetched token info for: {address}")
            state['token_info'] = result['token_info']
    return state

async def fetch_top_gainers(state: AgentState) -> AgentState:
    """Node: Fetch top gainers"""
    tool = next(t for t in tools if t.name == "coingecko_get_top_gainers")
    result = await tool._arun(json.dumps({"duration": "24h", "top_coins": 10}))
    
    state['memory'].append("Fetched top 24h gainers")
    state['top_gainers'] = result['top_gainers']
    return state

async def llm_interaction(state: AgentState) -> AgentState:
    """Node: Use OpenAI's LLM for interaction based on token info."""
    if not state['token_info']:
        state['memory'].append("No token info available to analyze with LLM.")
        return state
    
    prompt = f"Please analyze the following token info and provide insights:\n{json.dumps(state['token_info'], indent=2)}"
    
    try:
        response = await asyncio.to_thread(lambda: openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        ))
        analysis = response['choices'][0]['message']['content']
        state['memory'].append("LLM analysis completed.")
        state['token_analysis'] = analysis
    except Exception as e:
        state['memory'].append(f"LLM interaction failed: {str(e)}")
    
    return state

# Build graph with unique node keys
graph = StateGraph(AgentState)

graph.add_node("node_trending_tokens", fetch_trending_tokens)
graph.add_node("node_price_data", fetch_price_data)
graph.add_node("node_token_info", fetch_token_info)
graph.add_node("node_top_gainers", fetch_top_gainers)
graph.add_node("node_llm_interaction", llm_interaction)

graph.set_entry_point("node_trending_tokens")
graph.add_edge("node_trending_tokens", "node_price_data")
graph.add_edge("node_price_data", "node_token_info")
graph.add_edge("node_token_info", "node_top_gainers")
graph.add_edge("node_top_gainers", "node_llm_interaction")

app = graph.compile()

async def main():
    initial_state = AgentState(
        memory=[],
        trending_tokens=None,
        price_data=None,
        token_info=None,
        top_gainers=None,
        token_analysis=None
    )
    return await app.ainvoke(initial_state)

if __name__ == "__main__":
    final_state = asyncio.run(main())
    
    # Print trending tokens (showing the top 5)
    trending_list = extract_trending_list(final_state['trending_tokens'])
    print("Trending Tokens:")
    for token in trending_list[:5]:
        item = token.get("item", {})
        print(f"- ID: {item.get('id')}, Name: {item.get('name')}, Symbol: {item.get('symbol')}")
    
    print("\nPrice Data for 5 Tokens:")
    print(json.dumps(final_state['price_data'], indent=2))
    
    if final_state['token_info']:
        token_info = final_state['token_info']
        minimal_info = {
            "id": token_info.get("id"),
            "name": token_info.get("name"),
            "symbol": token_info.get("symbol"),
        }
        data = token_info.get("data", {})
        if data:
            minimal_info["price"] = data.get("price")
            minimal_info["market_cap"] = data.get("market_cap")
        print("\nMinimal Final Token Info:")
        print(json.dumps(minimal_info, indent=2))
    
    print("\nLLM Analysis:")
    print(final_state.get("token_analysis"))
    
    print("\nMemory History:")
    for entry in final_state['memory']:
        print(f"- {entry}")
