import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SquadsCreateMultisigTool(BaseTool):
    name: str = "squads_create_multisig"
    description: str = """
    Creates a Squads multisig wallet using SquadsManager.

    Input: A JSON string with:
    {
        "creator": "string, the creator's public key"
    }
    Output:
    {
        "multisig_details": "dict, multisig wallet details",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "creator": str
            }
            validate_input(data, schema)
            
            multisig_details = await self.agent_kit.create_squads_multisig(
                creator=data["creator"]
            )
            return {
                "multisig_details": multisig_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "multisig_details": None,
                "message": f"Error creating Squads multisig wallet: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
