
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit

class RugCheckFetchMostViewedTokensTool(BaseTool):
    name: str = "rugcheck_fetch_most_viewed_tokens"
    description: str = """
    Fetches the most viewed tokens using RugCheckManager.

    Input: None
    Output:
    {
        "most_viewed_tokens": "list, a list of the most viewed tokens",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self):
        try:
            most_viewed_tokens = await self.agent_kit.fetch_most_viewed_tokens()
            return {
                "most_viewed_tokens": most_viewed_tokens,
                "message": "Success"
            }
        except Exception as e:
            return {
                "most_viewed_tokens": None,
                "message": f"Error fetching most viewed tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
