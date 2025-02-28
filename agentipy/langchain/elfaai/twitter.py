import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class ElfaAiGetSmartTwitterAccountStatsTool(BaseTool):
    name: str = "elfa_ai_get_smart_twitter_account_stats"
    description: str = """
    Retrieves smart Twitter account statistics using ElfaAiManager.

    Input: A JSON string with:
    {
        "username": "string, the Twitter username"
    }
    Output:
    {
        "account_stats": "dict, the Twitter account statistics",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "username": {"type": str, "required": True}
            }
            validate_input(data, schema)
            account_stats = await self.agent_kit.get_smart_twitter_account_stats(
                username=data["username"]
            )
            return {
                "account_stats": account_stats,
                "message": "Success"
            }
        except Exception as e:
            return {
                "account_stats": None,
                "message": f"Error fetching smart Twitter account stats: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
