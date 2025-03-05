import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaRaydiumSellTool(BaseTool):
    name: str = "raydium_sell"
    description: str = """
    Sell tokens using Raydium's swap functionality.

    Input (JSON string):
    {
        "pair_address": "address_of_the_trading_pair",
        "percentage": 100,  # Percentage of tokens to sell (optional, defaults to 100)
        "slippage": 5  # Slippage tolerance in percentage (optional, defaults to 5)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
          
            data = json.loads(input)
            schema = {
                "pair_address": { "type": str, "required": True },
                "percentage": { "type": int, "required": False, "default": 100 },
                "slippage": { "type": int, "required": False, "default": 5 }
            }
            validate_input(data, schema)
            
            pair_address = data["pair_address"]
            percentage = data.get("percentage", 100)  # Default to 100% if not provided
            slippage = data.get("slippage", 5)  # Default to 5% slippage if not provided

            result = await self.solana_kit.sell_with_raydium(pair_address, percentage, slippage)

            return {
                "status": "success",
                "message": "Sell transaction completed successfully",
                "pair_address": pair_address,
                "percentage": percentage,
                "slippage": slippage,
                "transaction": result,
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
