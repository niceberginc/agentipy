import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SquadsCreateMultisigProposalTool(BaseTool):
    name: str = "squads_create_multisig_proposal"
    description: str = """
    Creates a multisig proposal using SquadsManager.

    Input: A JSON string with:
    {
        "transaction_index": "int, the transaction index for the proposal"
    }
    Output:
    {
        "proposal_details": "dict, proposal details",
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
            proposal_details = await self.agent_kit.create_multisig_proposal(
                transaction_index=data["transaction_index"]
            )
            return {
                "proposal_details": proposal_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "proposal_details": None,
                "message": f"Error creating multisig proposal: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")