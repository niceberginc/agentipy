import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class SolanaHeliusGetMintlistsTool(BaseTool):
    name: str = "solana_helius_get_mintlists"
    description: str = """
    Fetch mintlists for a given list of verified creators.

    Input: A JSON string with:
    {
        "first_verified_creators": "List of first verified creator addresses",
        "verified_collection_addresses": "Optional list of verified collection addresses",
        "limit": "Optional limit for results",
        "pagination_token": "Optional pagination token"
    }

    Output: {
        "mintlists": List[dict], # list of mintlists matching the criteria
        "status": "success" or "error",
        "message": "Error message if any"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "first_verified_creators": {"type": list, "required": True},
                "verified_collection_addresses": {"type": list, "required": False},
                "limit": {"type": int, "required": False},
                "pagination_token": {"type": str, "required": False}
            }
            validate_input(data, schema)

            result = await self.solana_kit.get_mintlists(
                first_verified_creators=data["first_verified_creators"],
                verified_collection_addresses=data.get("verified_collection_addresses"),
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
