import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class ElfaAiGetSmartMentionsTool(BaseTool):
    name: str = "elfa_ai_get_smart_mentions"
    description: str = """
    Retrieves smart mentions from Elfa AI using ElfaAiManager.

    Input: A JSON string with:
    {
        "limit": "int, optional, the number of mentions to retrieve (default: 100)",
        "offset": "int, optional, the offset for pagination (default: 0)"
    }
    Output:
    {
        "mentions_data": "dict, the smart mentions data",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "limit": {"type": int, "required": False},
                "offset": {"type": int, "required": False}
            }
            validate_input(data, schema)
            mentions_data = await self.agent_kit.get_smart_mentions(
                limit=data.get("limit", 100),
                offset=data.get("offset", 0)
            )
            return {
                "mentions_data": mentions_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "mentions_data": None,
                "message": f"Error fetching smart mentions: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


class ElfaAiGetTopMentionsByTickerTool(BaseTool):
    name: str = "elfa_ai_get_top_mentions_by_ticker"
    description: str = """
    Retrieves top mentions by ticker using ElfaAiManager.

    Input: A JSON string with:
    {
        "ticker": "string, the ticker symbol",
        "time_window": "string, optional, the time window for mentions (default: '1h')",
        "page": "int, optional, the page number (default: 1)",
        "page_size": "int, optional, the number of results per page (default: 10)",
        "include_account_details": "bool, optional, whether to include account details (default: False)"
    }
    Output:
    {
        "mentions_data": "dict, the mentions data for the given ticker",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "ticker": {"type": str, "required": True},
                "time_window": {"type": str, "required": False},
                "page": {"type": int, "required": False},
                "page_size": {"type": int, "required": False},
                "include_account_details": {"type": bool, "required": False}
            }
            validate_input(data, schema)
            mentions_data = await self.agent_kit.get_top_mentions_by_ticker(
                ticker=data["ticker"],
                time_window=data.get("time_window", "1h"),
                page=data.get("page", 1),
                page_size=data.get("page_size", 10),
                include_account_details=data.get("include_account_details", False)
            )
            return {
                "mentions_data": mentions_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "mentions_data": None,
                "message": f"Error fetching top mentions by ticker: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


class ElfaAiSearchMentionsByKeywordsTool(BaseTool):
    name: str = "elfa_ai_search_mentions_by_keywords"
    description: str = """
    Searches mentions by keywords using ElfaAiManager.

    Input: A JSON string with:
    {
        "keywords": "string, keywords for search",
        "from_timestamp": "int, the start timestamp",
        "to_timestamp": "int, the end timestamp",
        "limit": "int, optional, the number of results to fetch (default: 20)",
        "cursor": "string, optional, the cursor for pagination"
    }
    Output:
    {
        "search_results": "dict, the search results",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "keywords": {"type": str, "required": True},
                "from_timestamp": {"type": int, "required": True},
                "to_timestamp": {"type": int, "required": True},
                "limit": {"type": int, "required": False},
                "cursor": {"type": str, "required": False}
            }
            validate_input(data, schema)
            search_results = await self.agent_kit.search_mentions_by_keywords(
                keywords=data["keywords"],
                from_timestamp=data["from_timestamp"],
                to_timestamp=data["to_timestamp"],
                limit=data.get("limit", 20),
                cursor=data.get("cursor")
            )
            return {
                "search_results": search_results,
                "message": "Success"
            }
        except Exception as e:
            return {
                "search_results": None,
                "message": f"Error searching mentions by keywords: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
