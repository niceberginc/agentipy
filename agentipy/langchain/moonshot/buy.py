import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaBuyUsingMoonshotTool(BaseTool):
    name: str = "solana_buy_using_moonshot"
    description:str = """
    Buy a token using Moonshot.

    Input: A JSON string with:
    {
        "mint_str": "string, the mint address of the token to buy",
        "collateral_amount": 0.01, # optional, collateral amount in SOL to use for the purchase (default: 0.01)
        "slippage_bps": 500 # optional, slippage in basis points (default: 500)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "mint_str": {"type": str, "required": True},
                "collateral_amount": {"type": float, "required": False, "min": 0},
                "slippage_bps": {"type": int, "required": False, "min": 0, "max": 10000}
            }
            validate_input(data, schema)

            mint_str = data["mint_str"]
            collateral_amount = data.get("collateral_amount", 0.01)
            slippage_bps = data.get("slippage_bps", 500)
            
            result = await self.solana_kit.buy_using_moonshot(mint_str, collateral_amount, slippage_bps)

            return {
                "status": "success",
                "message": "Token purchased successfully using Moonshot.",
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
  