from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit

class RugCheckFetchNewTokensTool(BaseTool):
    name: str = "rugcheck_fetch_new_tokens"
    description: str = """
    Fetches new tokens using RugCheckManager.

    Input: None
    Output:
    {
        "new_tokens": "list, a list of new tokens",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self):
        try:
            new_tokens = await self.agent_kit.fetch_new_tokens()
            return {
                "new_tokens": new_tokens,
                "message": "Success"
            }
        except Exception as e:
            return {
                "new_tokens": None,
                "message": f"Error fetching new tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
