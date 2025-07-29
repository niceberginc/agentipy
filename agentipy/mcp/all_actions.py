from agentipy.mcp.allora import ALLORA_ACTIONS
from agentipy.mcp.coingecko import COINGECKO_ACTIONS
from agentipy.mcp.core import CORE_ACTIONS
from agentipy.mcp.debridge import DEBRIDGE_ACTIONS
from agentipy.mcp.dexscreener import TOKEN_DATA_ACTIONS
from agentipy.mcp.jito import JITO_ACTIONS
from agentipy.mcp.jupiter import JUPITER_ACTIONS
from agentipy.mcp.lulo import LULO_ACTIONS
from agentipy.mcp.pyth import PYTH_ACTIONS

ALL_ACTIONS = {
    **CORE_ACTIONS,
    **ALLORA_ACTIONS,
    **JUPITER_ACTIONS,
    **COINGECKO_ACTIONS,
    **PYTH_ACTIONS,
    **DEBRIDGE_ACTIONS,
    **LULO_ACTIONS,
    **JITO_ACTIONS,
    **TOKEN_DATA_ACTIONS
}
