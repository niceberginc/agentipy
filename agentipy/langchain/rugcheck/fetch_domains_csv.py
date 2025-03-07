import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class RugCheckFetchDomainsCSVTool(BaseTool):
    name: str = "rugcheck_fetch_domains_csv"
    description: str = """
    Fetches all registered domains in CSV format using RugCheckManager.

    Input: A JSON string with:
    {
        "verified": "bool, optional, filter for verified domains (default: False)"
    }
    Output:
    {
        "csv_data": "string, the CSV string containing all registered domains",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "verified": {"type": bool, "required": False}
            }
            validate_input(data, schema)
            csv_data = await self.agent_kit.fetch_domains_csv(
                verified=data.get("verified", False)
            )
            return {
                "csv_data": csv_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "csv_data": None,
                "message": f"Error fetching domains CSV: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
