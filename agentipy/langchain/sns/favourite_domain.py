import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaSNSGetFavouriteDomainTool(BaseTool):
    name: str = "solana_sns_get_favourite_domain"
    description: str = """
    Fetches the favorite domain of a given owner using Solana Name Service.

    Input: A JSON string with:
    {
        "owner": "string, the base58-encoded public key of the domain owner"
    }

    Output:
    {
        "domain": "string, the favorite domain of the owner",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "owner": {"type": str, "required": True}
            }
            validate_input(data, schema)

            owner = data["owner"]
            if not owner:
                raise ValueError("Owner address is required.")

            domain = await self.solana_kit.get_favourite_domain(owner)
            return {
                "domain": domain or "Not Found",
                "message": "Success" if domain else "No favorite domain found for this owner."
            }
        except Exception as e:
            return {
                "domain": None,
                "message": f"Error fetching favorite domain: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
