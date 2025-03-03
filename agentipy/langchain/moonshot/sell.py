import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaSellUsingMoonshotTool(BaseTool):
    name: str = "solana_sell_using_moonshot"
    description:str = """
    Sell a token using Moonshot.

    Input: A JSON string with:
    {
        "mint_str": "string, the mint address of the token to sell",
        "token_balance": 0.01, # optional, token balance to sell (default: 0.01)
        "slippage_bps": 500 # optional, slippage in basis points (default: 500)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "mint_str": {"type": str, "required": True},
                "token_balance": {"type": float, "required": False, "min": 0},
                "slippage_bps": {"type": int, "required": False, "min": 0, "max": 10000}
            }
            validate_input(data, schema)

            mint_str = data["mint_str"]
            token_balance = data.get("token_balance", 0.01)
            slippage_bps = data.get("slippage_bps", 500)
            
            result = await self.solana_kit.sell_using_moonshot(mint_str, token_balance, slippage_bps)

            return {
                "status": "success",
                "message": "Token sold successfully using Moonshot.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
