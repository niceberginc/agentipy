from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit

class RugCheckFetchRecentlyVerifiedTokensTool(BaseTool):
    name: str = "rugcheck_fetch_recently_verified_tokens"
    description: str = """
    Fetches recently verified tokens using RugCheckManager.

    Input: None
    Output:
    {
        "recently_verified_tokens": "list, a list of recently verified tokens",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self):
        try:
            recently_verified_tokens = await self.agent_kit.fetch_recently_verified_tokens()
            return {
                "recently_verified_tokens": recently_verified_tokens,
                "message": "Success"
            }
        except Exception as e:
            return {
                "recently_verified_tokens": None,
                "message": f"Error fetching recently verified tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
