import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class GetOwnedAllDomainsTool(BaseTool):
    name: str = "get_owned_all_domains"
    description: str = """
    Retrieves all domains owned by a given user.

    Input: A JSON string with:
    {
        "owner": "string, the owner's public key"
    }
    Output:
    {
        "domains": "list of strings, owned domains",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "owner": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            owned_domains = await self.solana_kit.get_owned_all_domains(data["owner"])
            return {"domains": owned_domains, "message": "Success"} if owned_domains else {"message": "No owned domains found"}
        except Exception as e:
            return {"message": f"Error fetching owned domains: {str(e)}"}

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
 