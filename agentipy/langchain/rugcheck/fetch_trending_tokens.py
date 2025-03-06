from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit


class RugCheckFetchTrendingTokensTool(BaseTool):
    name: str = "rugcheck_fetch_trending_tokens"
    description: str = """
    Fetches trending tokens using RugCheckManager.

    Input: None
    Output:
    {
        "trending_tokens": "list, a list of trending tokens",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            trending_tokens = await self.agent_kit.fetch_trending_tokens()
            return {
                "trending_tokens": trending_tokens,
                "message": "Success"
            }
        except Exception as e:
            return {
                "trending_tokens": None,
                "message": f"Error fetching trending tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
