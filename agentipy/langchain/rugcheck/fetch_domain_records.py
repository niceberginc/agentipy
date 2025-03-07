import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class RugCheckFetchDomainRecordsTool(BaseTool):
    name: str = "rugcheck_fetch_domain_records"
    description: str = """
    Fetches all records for a domain using RugCheckManager.

    Input: A JSON string with:
    {
        "domain": "string, the domain name"
    }
    Output:
    {
        "records": "list, a list of all records for the domain",
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
            records = await self.agent_kit.fetch_domain_records(
                domain=data["domain"]
            )
            return {
                "records": records,
                "message": "Success"
            }
        except Exception as e:
            return {
                "records": None,
                "message": f"Error fetching domain records: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
