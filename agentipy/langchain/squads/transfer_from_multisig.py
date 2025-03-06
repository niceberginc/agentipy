import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SquadsTransferFromMultisigTreasuryTool(BaseTool):
    name: str = "squads_transfer_from_multisig_treasury"
    description: str = """
    Transfers funds from a multisig treasury using SquadsManager.

    Input: A JSON string with:
    {
        "amount": "float, the amount to transfer",
        "to": "string, the recipient's public key",
        "vault_index": "int, the vault index",
        "mint": "string, the mint address"
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
                "amount": "float",
                "to": "string",
                "vault_index": "int",
                "mint": "string"
            }
            validate_input(data, schema)
            
            transaction_details = await self.agent_kit.transfer_from_multisig_treasury(
                amount=data["amount"],
                to=data["to"],
                vault_index=data["vault_index"],
                mint=data["mint"]
            )
            return {
                "transaction_details": transaction_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_details": None,
                "message": f"Error transferring from multisig treasury: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")