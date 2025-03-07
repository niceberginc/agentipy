import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class VoltrDepositStrategyTool(BaseTool):
    name: str = "voltr_deposit_strategy"
    description: str = """
    Deposits funds into a Voltr strategy.

    Input: A JSON string with:
    {
        "deposit_amount": "string, the deposit amount",
        "vault": "string, the vault address",
        "strategy": "string, the strategy address"
    }

    Output:
    {
        "transaction_details": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "deposit_amount": {"type": str, "required": True},
                "vault": {"type": str, "required": True},
                "strategy": {"type": str, "required": True},
            }
            validate_input(data, schema)

            deposit_amount = data["deposit_amount"]
            vault = data["vault"]
            strategy = data["strategy"]

            result = await self.solana_kit.deposit_strategy(deposit_amount, vault, strategy)
            return {
                "status": "success",
                "transaction_details": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")