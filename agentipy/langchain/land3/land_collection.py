import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class Create3LandCollectionTool(BaseTool):
    name: str = "create_3land_collection"
    description: str = """
    Creates a 3Land NFT collection.

    Input: A JSON string with:
    {
        "collection_symbol": "string, symbol of the collection",
        "collection_name": "string, name of the collection",
        "collection_description": "string, description of the collection",
        "main_image_url": "string, optional, URL of the main image",
        "cover_image_url": "string, optional, URL of the cover image",
        "is_devnet": "bool, optional, whether to use devnet"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "collection_symbol": {"type": str, "required": True},
                "collection_name": {"type": str, "required": True},
                "collection_description": {"type": str, "required": True},
                "main_image_url": {"type": str, "required": False},
                "cover_image_url": {"type": str, "required": False},
                "is_devnet": {"type": bool, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)

            
            
            transaction = await self.solana_kit.create_3land_collection(
                collection_symbol=data["collection_symbol"],
                collection_name=data["collection_name"],
                collection_description=data["collection_description"],
                main_image_url=data.get("main_image_url"),
                cover_image_url=data.get("cover_image_url"),
                is_devnet=data.get("is_devnet", False),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error creating 3land collection: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
