from mcp.types import Tool

from agentipy.tools.use_lulo import LuloManager

LULO_ACTIONS = {
    "LEND_ASSET": Tool(
        name="LEND_ASSET",
        description="Lend tokens for yields using Lulo API. input_schema Example: { amount: number }",
        inputSchema={
            "amount": {
                "type": "number",
                "description": "Amount of USDC to lend"
            },
        },
        handler=lambda agent, params: LuloManager.lend_asset(agent, params["amount"]),
    ),
    "LULO_LEND": Tool(
        name="CREATE_LULO",
        description="Lend tokens for yields using Lulo API. input_schema Example: { mint_address: string, amount: number }",
        inputSchema={
            "mint_address": {
                "type": "string",
                "description": "Mint address of the token to lend"
            },
            "amount": {
                "type": "number",
                "description": "Amount of tokens to lend"
            },
        },
        handler=lambda agent, params: LuloManager.lulo_lend(agent,params["mint_address"], params["amount"]),
    ),
    "LULO_WITHDRAW": Tool(
        name="LULO_WITHDRAW",
        description="Withdraw tokens from Lulo. input_schema Example: { mint_address: string, amount: number }",
        inputSchema={
            "mint_address": {
                "type": "string",
                "description": "Mint address of the token to withdraw"
            },
            "amount": {
                "type": "number",
                "description": "Amount of tokens to withdraw"
            },
        },
        handler=lambda agent, params: LuloManager.lulo_withdraw(agent, params["mint_address"], params["amount"]),
    ),
}