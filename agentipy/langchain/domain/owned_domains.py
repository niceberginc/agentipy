import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class GetOwnedDomainsForTLDTool(BaseTool):
    name: str = "get_owned_domains_for_tld"
    description: str = """
    Retrieves the domains owned by the user for a given TLD.

    Input: A JSON string with:
    {
        "tld": "string, the top-level domain (TLD)"
    }
    Output:
    {
        "domains": "list of strings, owned domains under the TLD",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "tld": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            owned_domains = await self.solana_kit.get_owned_domains_for_tld(data["tld"])
            return {"domains": owned_domains, "message": "Success"} if owned_domains else {"message": "No owned domains found"}
        except Exception as e:
            return {"message": f"Error fetching owned domains: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
