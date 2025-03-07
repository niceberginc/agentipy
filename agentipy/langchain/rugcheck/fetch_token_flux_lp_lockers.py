import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class RugCheckFetchTokenFluxLPLockersTool(BaseTool):
    name: str = "rugcheck_fetch_token_flux_lp_lockers"
    description: str = """
    Fetches token flux LP lockers using RugCheckManager.

    Input: A JSON string with:
    {
        "token_id": "string, the ID of the token"
    }
    Output:
    {
        "flux_lp_lockers": "list, a list of token flux LP lockers",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "token_id": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            flux_lp_lockers = await self.agent_kit.fetch_token_flux_lp_lockers(
                token_id=data["token_id"]
            )
            return {
                "flux_lp_lockers": flux_lp_lockers,
                "message": "Success"
            }
        except Exception as e:
            return {
                "flux_lp_lockers": None,
                "message": f"Error fetching token flux LP lockers: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
