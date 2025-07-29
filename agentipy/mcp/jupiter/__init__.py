from mcp.types import Tool

from agentipy.tools.stake_with_jup import StakeManager
from agentipy.tools.trade import TradeManager

JUPITER_ACTIONS = {
    "STAKE_WITH_JUP": Tool(
        name="STAKE_WITH_JUP",
        description="Stake SOL with Jupiter. input_schema Example: { amount: number }",
        inputSchema={
            "amount": {
                "type": "number",
                "description": "Amount of SOL to stake"
            }
        },
        handler=lambda agent, params: StakeManager.stake_with_jup(
            agent,
            amount=params["amount"],
        ),
    ),
    "TRADE_WITH_JUP": Tool(
        name="TRADE_WITH_JUP",
        description=(
            "Trade a token with Jupiter. "
            "If a token ticker (like 'WIF' or 'BONK') is provided instead of a mint address,"
            "you should first call TOKEN_GET_ADDRESS_FROM_TICKER tool to resolve it. "
            "input_schema Example: { output_mint: string, input_amount: number, input_mint: string = 'So11111111111111111111111111111111111111112', slippage_bps: number = 50 }"
        ),
        inputSchema={
            "output_mint": {"type": "string", "description": "Token to receive (mint address or ticker)"},
            "input_amount": {"type": "number", "description": "Amount of token to swap from"},
            "input_mint": {"type": "string", "description": "Token to swap from (mint address or ticker)"},
            "slippage_bps": {
                "type": "number",
                "description": "Slippage in basis points. Defaults to 50",
                "default": 50
            },
        },
        handler=lambda agent, params: TradeManager.trade(
            agent,
            output_mint=params["output_mint"],
            input_amount=params["input_amount"],
            input_mint=params["input_mint"],
            slippage_bps=params.get("slippage_bps", 50),
        ),
    ),
}
