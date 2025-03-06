import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SquadsDepositToMultisigTreasuryTool(BaseTool):
    name: str = "squads_deposit_to_multisig_treasury"
    description: str = """
    Deposits funds to a multisig treasury using SquadsManager.

    Input: A JSON string with:
    {
        "amount": "float, the amount to deposit",
        "vault_index": "int, the vault index",
        "mint": "string, optional, the mint address"
    }
    Output:
    {
        "transaction_details": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "amount": float,
                "vault_index": int,
                "mint": str
            }
            validate_input(data, schema)
            transaction_details = await self.agent_kit.deposit_to_multisig_treasury(
                amount=data["amount"],
                vault_index=data["vault_index"],
                mint=data.get("mint")
            )
            return {
                "transaction_details": transaction_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_details": None,
                "message": f"Error depositing to multisig treasury: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")