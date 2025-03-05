import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class RugCheckLookupDomainTool(BaseTool):
    name: str = "rugcheck_lookup_domain"
    description: str = """
    Looks up a domain by name using RugCheckManager.

    Input: A JSON string with:
    {
        "domain": "string, the domain name to look up"
    }
    Output:
    {
        "domain_details": "dict, the details of the domain",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "domain": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            domain_details = await self.agent_kit.lookup_domain(
                domain=data["domain"]
            )
            return {
                "domain_details": domain_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "domain_details": None,
                "message": f"Error looking up domain: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
