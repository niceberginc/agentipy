import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class SolanaGetMetaplexAssetTool(BaseTool):
    name: str = "solana_get_metaplex_asset"
    description: str = """
    Fetches detailed information about a specific Metaplex asset.

    Input: A JSON string with:
    {
        "asset_id": "string, the unique identifier of the asset"
    }

    Output:
    {
        "success": "bool, whether the operation was successful",
        "value": "object, detailed asset information if successful",
        "message": "string, additional details or error information"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "asset_id": {"type": str, "required": True}
            }
            validate_input(data, schema)

            asset_id = data["asset_id"]

            result = await self.solana_kit.get_metaplex_asset(asset_id)
            return result
        except Exception as e:
            return {"success": False, "message": f"Error fetching Metaplex asset: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
