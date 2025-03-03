import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaRaydiumBuyTool(BaseTool):
    name: str = "raydium_buy"
    description: str = """
    Buy tokens using Raydium's swap functionality.

    Input (JSON string):
    {
        "pair_address": "address_of_the_trading_pair",
        "sol_in": 0.01,  # Amount of SOL to spend (optional, defaults to 0.01)
        "slippage": 5  # Slippage tolerance in percentage (optional, defaults to 5)
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
         
            data = json.loads(input)
            schema = {
                "pair_address": { "type": str, "required": True },
                "sol_in": { "type": float, "required": False,  },
                "slippage": { "type": int, "required": False,  }
            }

            
            validate_input(data, schema)
    
           
            pair_address = data["pair_address"]
            sol_in = data.get("sol_in", 0.01)  # Default to 0.01 SOL if not provided
            slippage = data.get("slippage", 5)  # Default to 5% slippage if not provided

            result = await self.solana_kit.buy_with_raydium(pair_address, sol_in, slippage)

            return {
                "status": "success",
                "message": "Buy transaction completed successfully",
                "pair_address": pair_address,
                "sol_in": sol_in,
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
