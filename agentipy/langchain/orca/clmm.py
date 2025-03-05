import json

from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool

from agentipy.helpers import validate_input

class OrcaCreateClmmTool(BaseTool):
    name: str = "orca_create_clmm"
    description: str = """
    Creates a Concentrated Liquidity Market Maker (CLMM) using OrcaManager.

    Input: A JSON string with:
    {
        "mint_deploy": "string, the deploy mint address",
        "mint_pair": "string, the paired mint address",
        "initial_price": "float, the initial price for the pool",
        "fee_tier": "string, the fee tier percentage"
    }
    Output:
    {
        "clmm_data": "dict, details of the created CLMM",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "mint_deploy": {"type": str, "required": True},
                "mint_pair": {"type": str, "required": True},
                "initial_price": {"type": float, "required": True},
                "fee_tier": {"type": str, "required": True}
            }
            validate_input(data, schema)
            clmm_data = await self.solana_kit.create_clmm(
                mint_deploy=data["mint_deploy"],
                mint_pair=data["mint_pair"],
                initial_price=data["initial_price"],
                fee_tier=data["fee_tier"]
            )
            return {
                "clmm_data": clmm_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "clmm_data": None,
                "message": f"Error creating CLMM: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
