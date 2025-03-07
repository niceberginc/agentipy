import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class SolanaHeliusGetActiveListingsTool(BaseTool):
    name: str = "solana_helius_get_active_listings"
    description: str = """
    Fetch active NFT listings from various marketplaces.

    Input: A JSON string with:
    {
        "first_verified_creators": ["string, the addresses of verified creators"],
        "verified_collection_addresses": ["optional list of verified collection addresses"],
        "marketplaces": ["optional list of marketplaces"],
        "limit": "optional limit to the number of listings",
        "pagination_token": "optional token for pagination"
    }

    Output:
    {
        "active_listings": "list of active NFT listings"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "first_verified_creators": {"type": list, "required": True},
                "verified_collection_addresses": {"type": list, "required": False},
                "marketplaces": {"type": list, "required": False},
                "limit": {"type": int, "required": False},
                "pagination_token": {"type": str, "required": False}
            }
            validate_input(data, schema)

            result = await self.solana_kit.get_active_listings(
                first_verified_creators=data["first_verified_creators"],
                verified_collection_addresses=data.get("verified_collection_addresses"),
                marketplaces=data.get("marketplaces"),
                limit=data.get("limit"),
                pagination_token=data.get("pagination_token")
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


