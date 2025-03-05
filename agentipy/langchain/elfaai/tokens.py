import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class ElfaAiGetTrendingTokensTool(BaseTool):
    name: str = "elfa_ai_get_trending_tokens"
    description: str = """
    Fetches trending tokens using Elfa AI with ElfaAiManager.

    Input: A JSON string with:
    {
        "time_window": "string, optional, the time window for trending tokens (default: '24h')",
        "page": "int, optional, the page number (default: 1)",
        "page_size": "int, optional, the number of results per page (default: 50)",
        "min_mentions": "int, optional, the minimum number of mentions required (default: 5)"
    }
    Output:
    {
        "trending_tokens": "dict, the trending tokens data",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "time_window": {"type": str, "required": False},
                "page": {"type": int, "required": False},
                "page_size": {"type": int, "required": False},
                "min_mentions": {"type": int, "required": False}
            }
            validate_input(data, schema)
            trending_tokens = await self.agent_kit.get_trending_tokens_using_elfa_ai(
                time_window=data.get("time_window", "24h"),
                page=data.get("page", 1),
                page_size=data.get("page_size", 50),
                min_mentions=data.get("min_mentions", 5)
            )
            return {
                "trending_tokens": trending_tokens,
                "message": "Success"
            }
        except Exception as e:
            return {
                "trending_tokens": None,
                "message": f"Error fetching trending tokens using Elfa AI: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
