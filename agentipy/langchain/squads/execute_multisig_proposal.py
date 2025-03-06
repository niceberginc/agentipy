import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SquadsExecuteMultisigProposalTool(BaseTool):
    name: str = "squads_execute_multisig_proposal"
    description: str = """
    Executes a multisig proposal using SquadsManager.

    Input: A JSON string with:
    {
        "transaction_index": "int, the transaction index to execute"
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
                "transaction_index": int
            }
            validate_input(data, schema)
            transaction_details = await self.agent_kit.execute_multisig_proposal(
                transaction_index=data["transaction_index"]
            )
            return {
                "transaction_details": transaction_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_details": None,
                "message": f"Error executing multisig proposal: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")