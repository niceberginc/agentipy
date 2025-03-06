
import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class OrcaCreateLiquidityPoolTool(BaseTool):
    name: str = "orca_create_liquidity_pool"
    description: str = """
    Creates a liquidity pool using OrcaManager.

    Input: A JSON string with:
    {
        "deposit_token_amount": "float, the amount of token to deposit",
        "deposit_token_mint": "string, the mint address of the deposit token",
        "other_token_mint": "string, the mint address of the paired token",
        "initial_price": "float, the initial price for the pool",
        "max_price": "float, the maximum price for the pool",
        "fee_tier": "string, the fee tier percentage"
    }
    Output:
    {
        "pool_data": "dict, details of the created liquidity pool",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "deposit_token_amount": {"type": float, "required": True},
                "deposit_token_mint": {"type": str, "required": True},
                "other_token_mint": {"type": str, "required": True},
                "initial_price": {"type": float, "required": True},
                "max_price": {"type": float, "required": True},
                "fee_tier": {"type": str, "required": True}
            }
            validate_input(data, schema)
            pool_data = await self.solana_kit.create_liquidity_pool(
                deposit_token_amount=data["deposit_token_amount"],
                deposit_token_mint=data["deposit_token_mint"],
                other_token_mint=data["other_token_mint"],
                initial_price=data["initial_price"],
                max_price=data["max_price"],
                fee_tier=data["fee_tier"]
            )
            return {
                "pool_data": pool_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "pool_data": None,
                "message": f"Error creating liquidity pool: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

