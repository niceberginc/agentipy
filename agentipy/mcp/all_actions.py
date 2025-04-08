from agentipy.mcp.allora import ALLORA_ACTIONS
from agentipy.mcp.coingecko import COINGECKO_ACTIONS
from agentipy.mcp.core import SOLANA_ACTIONS
from agentipy.mcp.debridge import DEBRIDGE_ACTIONS
from agentipy.mcp.jupiter import JUPITER_ACTIONS
from agentipy.mcp.pyth import PYTH_ACTIONS

ALL_ACTIONS = {
    **SOLANA_ACTIONS,
    **ALLORA_ACTIONS,
    **JUPITER_ACTIONS,
    **COINGECKO_ACTIONS,
    **PYTH_ACTIONS,
    **DEBRIDGE_ACTIONS,
}
