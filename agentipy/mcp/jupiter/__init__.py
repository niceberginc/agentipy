from mcp.types import Tool

from agentipy.tools.stake_with_jup import StakeManager
from agentipy.tools.trade import TradeManager

JUPITER_ACTIONS = {
    "STAKE_WITH_JUP": Tool(
        name="STAKE_WITH_JUP",
        description="Stake SOL with Jupiter",
        inputSchema={"amount": {"type": "number", "description": "Amount of SOL to stake"}},
        handler=lambda agent, params: StakeManager.stake_with_jup(
            agent,
            amount=params["amount"],
        ),
    ),
    "TRADE_WITH_JUP": Tool(
        name="TRADE_WITH_JUP",
        description="Trade a token with Jupiter",
        inputSchema={
            "output_mint": {"type": "string", "description": "Token to trade"},
            "input_amount": {"type": "number", "description": "Amount of token to trade"},
            "input_mint": {"type": "string", "description": "Token to trade"},
            "slippage_bps": {"type": "number", "description": "Slippage in basis points"},
        },
        handler=lambda agent, params: TradeManager.trade(
            agent,
            output_mint=params["output_mint"],
            input_amount=params["input_amount"],
            input_mint=params["input_mint"],
            slippage_bps=params["slippage_bps"],
        ),
    ),
}
