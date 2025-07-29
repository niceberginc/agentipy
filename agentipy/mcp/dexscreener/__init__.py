from mcp.types import Tool
from agentipy.tools.get_token_data import TokenDataManager

TOKEN_DATA_ACTIONS = {
    "TOKEN_GET_DATA_BY_ADDRESS": Tool(
        name="TOKEN_GET_DATA_BY_ADDRESS",
        description="Get token data using its mint address on Solana. input_schema Example: { mint: string }",
        inputSchema={
            "mint": {
                "type": "string",
                "description": "Solana mint address of the token",
            },
        },
        handler=lambda agent, params: TokenDataManager.get_token_data_by_address(
            mint=params["mint"]
        ),
    ),

    "TOKEN_GET_ADDRESS_FROM_TICKER": Tool(
        name="TOKEN_GET_ADDRESS_FROM_TICKER",
        description="Get Solana token address from ticker symbol using DexScreener. input_schema Example: { ticker: string }",
        inputSchema={
            "ticker": {
                "type": "string",
                "description": "Ticker symbol (e.g., BONK, WIF)",
            },
        },
        handler=lambda agent, params: TokenDataManager.get_token_address_from_ticker(
            ticker=params["ticker"]
        ),
    ),

    "TOKEN_GET_DATA_BY_TICKER": Tool(
        name="TOKEN_GET_DATA_BY_TICKER",
        description="Get full token data using a ticker symbol. Combines address resolution and metadata fetch. input_schema Example: { ticker: string }",
        inputSchema={
            "ticker": {
                "type": "string",
                "description": "Ticker symbol (e.g., BONK, WIF)",
            },
        },
        handler=lambda agent, params: TokenDataManager.get_token_data_by_ticker(
            ticker=params["ticker"]
        ),
    ),
}
