import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool

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

class GetAllDomainsTLDsTool(BaseTool):
    name: str = "get_all_domains_tlds"
    description: str = """
    Retrieves all available top-level domains (TLDs).

    Input: No input required.
    Output:
    {
        "tlds": "list of strings, available TLDs",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            tlds = await self.solana_kit.get_all_domains_tlds()
            return {"tlds": tlds, "message": "Success"} if tlds else {"message": "No TLDs found"}
        except Exception as e:
            return {"message": f"Error fetching TLDs: {str(e)}"}

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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
  

def get_domain_tools(solana_kit: SolanaAgentKit):
    return [
        ResolveAllDomainsTool(solana_kit=solana_kit),
        GetOwnedDomainsForTLDTool(solana_kit=solana_kit),
        GetAllDomainsTLDsTool(solana_kit=solana_kit),
        GetOwnedAllDomainsTool(solana_kit=solana_kit)
    ]
