import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit



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
