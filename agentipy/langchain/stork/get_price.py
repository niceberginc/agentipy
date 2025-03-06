import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class StorkGetPriceTool(BaseTool):
    name: str = "stork_get_price"
    description: str = """
    Fetch the price of an asset using the Stork Oracle.

    Input: A JSON string with:
    {
        "asset_id": "string, the asset pair ID to fetch price data for (e.g., SOLUSD)."
    }

    Output:
    {
        "price": float, # the token price,
        "timestamp": int, # the unix nanosecond timestamp of the price
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "asset_id": {"type": str, "required": True}
            }
            validate_input(data, schema)
            asset_id = data["asset_id"]
            
            result = await self.solana_kit.stork_fetch_price(asset_id)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
