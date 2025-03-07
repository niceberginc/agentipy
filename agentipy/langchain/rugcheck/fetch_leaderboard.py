from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit


class RugCheckFetchLeaderboardTool(BaseTool):
    name: str = "rugcheck_fetch_leaderboard"
    description: str = """
    Fetches the leaderboard using RugCheckManager.

    Input: None
    Output:
    {
        "leaderboard": "list, a list of leaderboard entries",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self):
        try:
            leaderboard = await self.agent_kit.fetch_leaderboard()
            return {
                "leaderboard": leaderboard,
                "message": "Success"
            }
        except Exception as e:
            return {
                "leaderboard": None,
                "message": f"Error fetching leaderboard: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
