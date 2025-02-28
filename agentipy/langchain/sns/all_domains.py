import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaSNSGetAllDomainsTool(BaseTool):
    name: str = "solana_sns_get_all_domains"
    description: str = """
    Fetches all domains associated with a given owner using Solana Name Service.

    Input: A JSON string with:
    {
        "owner": "string, the base58-encoded public key of the domain owner"
    }

    Output:
    {
        "domains": ["string", "string", ...], # List of domains owned by the owner
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
            
            domains = await self.solana_kit.get_all_domains_for_owner(owner)
            return {
                "domains": domains or [],
                "message": "Success" if domains else "No domains found for this owner."
            }
        except Exception as e:
            return {
                "domains": [],
                "message": f"Error fetching domains: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
