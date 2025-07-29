from mcp.types import Tool

from agentipy.tools.use_pyth import PythManager

PYTH_ACTIONS = {
    "PYTH_GET_PRICE": Tool(
        name="PYTH_GET_PRICE",
        description="Get the price of a coin from Pyth. input_schema Example: { base_token_ticker: string, quote_token_ticker: string }",
        inputSchema={
            "base_token_ticker": {
                "type": "string",
                "description": "Base token ticker to get the price for",
            },
            "quote_token_ticker": {
                "type": "string",
                "description": "Quote token ticker to get the price in",
            },
        },
        handler=lambda agent, params: PythManager.get_price(
            agent,
            base_token_ticker=params["base_token_ticker"],
            quote_token_ticker=params["quote_token_ticker"],
        ),
    ),
}
