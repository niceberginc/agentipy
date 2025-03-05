import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class RugCheckFetchAllDomainsTool(BaseTool):
    name: str = "rugcheck_fetch_all_domains"
    description: str = """
    Fetches all registered domains with optional pagination and filtering using RugCheckManager.

    Input: A JSON string with:
    {
        "page": "int, optional, the page number for pagination (default: 1)",
        "limit": "int, optional, the number of records per page (default: 50)",
        "verified": "bool, optional, filter for verified domains (default: False)"
    }
    Output:
    {
        "domains": "list, a list of all registered domains",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "page": {"type": int, "required": False},
                "limit": {"type": int, "required": False},
                "verified": {"type": bool, "required": False}
            }
            validate_input(data, schema)
            domains = await self.agent_kit.fetch_all_domains(
                page=data.get("page", 1),
                limit=data.get("limit", 50),
                verified=data.get("verified", False)
            )
            return {
                "domains": domains,
                "message": "Success"
            }
        except Exception as e:
            return {
                "domains": None,
                "message": f"Error fetching all domains: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
