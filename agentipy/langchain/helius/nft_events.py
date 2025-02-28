import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaHeliusGetNftEventsTool(BaseTool):
    name: str = "solana_helius_get_nft_events"
    description: str = """
    Fetch NFT events based on the given parameters.

    Input: A JSON string with:
    {
        "accounts": "List of addresses to fetch NFT events for",
        "types": "Optional list of event types",
        "sources": "Optional list of sources",
        "start_slot": "Optional start slot",
        "end_slot": "Optional end slot",
        "start_time": "Optional start time",
        "end_time": "Optional end time",
        "first_verified_creator": "Optional list of verified creators",
        "verified_collection_address": "Optional list of verified collection addresses",
        "limit": "Optional limit for results",
        "sort_order": "Optional sort order",
        "pagination_token": "Optional pagination token"
    }

    Output: {
        "events": List[dict], # list of NFT events matching the criteria
        "status": "success" or "error",
        "message": "Error message if any"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "accounts": {"type": list, "required": True},
                "types": {"type": list, "required": False},
                "sources": {"type": list, "required": False},
                "start_slot": {"type": int, "required": False},
                "end_slot": {"type": int, "required": False},
                "start_time": {"type": int, "required": False},
                "end_time": {"type": int, "required": False},
                "first_verified_creator": {"type": list, "required": False},
                "verified_collection_address": {"type": list, "required": False},
                "limit": {"type": int, "required": False},
                "sort_order": {"type": str, "required": False},
                "pagination_token": {"type": str, "required": False}
            }
            validate_input(data, schema)

            accounts = data["accounts"]
            types = data.get("types")
            sources = data.get("sources")
            start_slot = data.get("start_slot")
            end_slot = data.get("end_slot")
            start_time = data.get("start_time")
            end_time = data.get("end_time")
            first_verified_creator = data.get("first_verified_creator")
            verified_collection_address = data.get("verified_collection_address")
            limit = data.get("limit")
            sort_order = data.get("sort_order")
            pagination_token = data.get("pagination_token")

            result = await self.solana_kit.get_nft_events(
                accounts, types, sources, start_slot, end_slot, start_time, end_time, first_verified_creator, verified_collection_address, limit, sort_order, pagination_token
            )
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
