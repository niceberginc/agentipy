import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class VoltrWithdrawStrategyTool(BaseTool):
    name: str = "voltr_withdraw_strategy"
    description: str = """
    Withdraws funds from a Voltr strategy.

    Input: A JSON string with:
    {
        "withdraw_amount": "string, the withdrawal amount",
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
                "withdraw_amount": {"type": str, "required": True},
                "vault": {"type": str, "required": True},
                "strategy": {"type": str, "required": True},
            }
            validate_input(data, schema)

            withdraw_amount = data["withdraw_amount"]
            vault = data["vault"]
            strategy = data["strategy"]

            result = await self.solana_kit.withdraw_strategy(withdraw_amount, vault, strategy)
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