from mcp.types import Tool

from agentipy.tools.use_coingecko import CoingeckoManager

COINGECKO_ACTIONS = {
    "COINGECKO_GET_COIN_PRICE_VS": Tool(
        name="COINGECKO_GET_COIN_PRICE_VS",
        description="Get the price of a coin in a specific currency from Coingecko. input_schema Example: { coin_ids: string, vs_currencies: string }",
        inputSchema={
            "coin_ids": {
                "type": "string",
                "description": "Comma-separated list of coin IDs to get the price for",
            },
            "vs_currencies": {
                "type": "string",
                "description": "Comma-separated list of currencies to get the price in",
            },
        },
        handler=lambda agent, params: CoingeckoManager.get_coin_price_vs(
            agent,
            coin_ids=[params["coin_ids"]],
            vs_currencies=[params["vs_currencies"]],
        ),
    ),

    "COINGECKO_GET_TOKEN_INFO": Tool(
        name="COINGECKO_GET_TOKEN_INFO",
        description="Get token information from Coingecko. input_schema Example: { token_address: string }",
        inputSchema={
            "token_address": {
                "type": "string",
                "description": "Token address to get information for",
            },
        },
        handler=lambda agent, params: CoingeckoManager.get_token_info(
            agent,
            token_address=params["token_address"],
        ),
    ),

    "COINGECKO_GET_TOP_GAINERS": Tool(
        name="COINGECKO_GET_TOP_GAINERS",
        description="Get the top gainers from Coingecko. input_schema Example: { duration: string, top_coins: number }",
        inputSchema={
            "duration": {
                "type": "string",
                "description": "Duration for top gainers (e.g., '1h', '24h', '7d')",
            },
            "top_coins": {
                "type": "integer",
                "description": "Number of top gainers to return",
            },
        },
        handler=lambda agent, params: CoingeckoManager.get_top_gainers(
            agent,
            duration=params["duration"],
            top_coins=params["top_coins"],
        ),
    ),

    "COINGECTO_GET_TRENDING_POOLS": Tool(
        name="COINGECTO_GET_TRENDING_POOLS",
        description="Get the trending pools from Coingecko. input_schema Example: { duration: string }",
        inputSchema={
            "duration": {
                "type": "string",
                "description": "Duration for trending pools (e.g., '1h', '24h', '7d')",
            },
        },
        handler=lambda agent, params: CoingeckoManager.get_trending_pools(
            agent,
            duration=params["duration"],
        ),
    ),

    "COINGECKO_GET_TRENDING_TOKENS": Tool(
        name="COINGECKO_GET_TRENDING_TOKENS",
        description="Get the trending tokens from Coingecko. input_schema Example: {}",
        inputSchema={},
        handler=lambda agent, params: CoingeckoManager.get_trending_tokens(agent),
    ),

    "COINGECKO_GET_TOKEN_PRICE_DATA": Tool(
        name="COINGECKO_GET_TOKEN_PRICE_DATA",
        description="Get token price data from Coingecko. input_schema Example: { token_addresses: array<string> }",
        inputSchema={
            "token_addresses": {
                "type": "array",
                "description": "List of token addresses to get price data for",
            },
        },
        handler=lambda agent, params: CoingeckoManager.get_token_price_data(
            agent,
            token_addresses=params["token_addresses"],
        ),
    ),

    "COINGECKO_GET_LATEST_POOLS": Tool(
        name="COINGECKO_GET_LATEST_POOLS",
        description="Get the latest pools from Coingecko. input_schema Example: {}",
        inputSchema={},
        handler=lambda agent, params: CoingeckoManager.get_latest_pools(agent),
    ),
}
