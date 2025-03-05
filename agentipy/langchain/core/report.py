import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool

from agentipy.helpers import validate_input



class SolanaFetchTokenReportSummaryTool(BaseTool):
    name: str = "solana_fetch_token_report_summary"
    description: str = """
    Fetch a summary report for a specific token.

    Input: A JSON string with:
    {
        "mint": "Mint address of the token"
    }

    Output:
    {
        "status": "success",
        "data": <TokenCheck object as a dictionary>
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        """
        Asynchronous implementation of the tool.
        """
        try:
            data = json.loads(input)
            schema = {
                "mint": {"type": str, "required": True}
            }
            validate_input(data, schema)

            mint = data["mint"]
            
            result = self.solana_kit.fetch_token_report_summary(mint)
            return {
                "status": "success",
                "data": result.dict(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self):
        """
        Synchronous version of the tool, not implemented for async-only tools.
        """
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
    
class SolanaFetchTokenDetailedReportTool(BaseTool):
    name: str = "solana_fetch_token_detailed_report"
    description: str = """
    Fetch a detailed report for a specific token.

    Input: A JSON string with:
    {
        "mint": "Mint address of the token"
    }

    Output:
    {
        "status": "success",
        "data": <TokenCheck object as a dictionary>
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        """
        Asynchronous implementation of the tool.
        """
        try:
            data = json.loads(input)
            schema = {
                "mint": {"type": str, "required": True}
            }
            validate_input(data, schema)

            mint = data["mint"]
            
            result = self.solana_kit.fetch_token_detailed_report(mint)
            return {
                "status": "success",
                "data": result.dict(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self):
        """
        Synchronous version of the tool, not implemented for async-only tools.
        """
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
