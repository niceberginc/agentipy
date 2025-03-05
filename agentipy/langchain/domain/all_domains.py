import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class ResolveAllDomainsTool(BaseTool):
    name: str = "resolve_all_domains"
    description: str = """
    Resolves all domain types associated with a given domain name.

    Input: A JSON string with:
    {
        "domain": "string, the domain name to resolve"
    }
    Output:
    {
        "tld": "string, the resolved domain's TLD",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "domain": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            domain_tld = await self.solana_kit.resolve_all_domains(data["domain"])
            return {"tld": domain_tld, "message": "Success"} if domain_tld else {"message": "Domain resolution failed"}
        except Exception as e:
            return {"message": f"Error resolving domain: {str(e)}"}

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
