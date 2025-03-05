import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class RugCheckFetchTokenVotesTool(BaseTool):
    name: str = "rugcheck_fetch_token_votes"
    description: str = """
    Fetches token votes using RugCheckManager.

    Input: A JSON string with:
    {
        "mint": "string, the mint address of the token"
    }
    Output:
    {
        "token_votes": "list, a list of token votes",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "mint": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            token_votes = await self.agent_kit.fetch_token_votes(
                mint=data["mint"]
            )
            return {
                "token_votes": token_votes,
                "message": "Success"
            }
        except Exception as e:
            return {
                "token_votes": None,
                "message": f"Error fetching token votes: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
