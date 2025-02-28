import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool

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

class Create3LandNFTTool(BaseTool):
    name: str = "create_3land_nft"
    description: str = """
    Creates a 3Land NFT.

    Input: A JSON string with:
    {
        "item_name": "string, name of the NFT",
        "seller_fee": "float, seller fee percentage",
        "item_amount": "int, number of NFTs to mint",
        "item_symbol": "string, symbol of the NFT",
        "item_description": "string, description of the NFT",
        "traits": "Any, NFT traits",
        "price": "float, optional, price of the NFT",
        "main_image_url": "string, optional, URL of the main image",
        "cover_image_url": "string, optional, URL of the cover image",
        "spl_hash": "string, optional, SPL hash identifier",
        "pool_name": "string, optional, pool name",
        "is_devnet": "bool, optional, whether to use devnet",
        "with_pool": "bool, optional, whether to include a pool"
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
                "item_name": {"type": str, "required": True},
                "seller_fee": {"type": float, "required": True},
                "item_amount": {"type": int, "required": True},
                "item_symbol": {"type": str, "required": True},
                "item_description": {"type": str, "required": True},
                "traits": {"type": str, "required": True},
                "price": {"type": float, "required": False},
                "main_image_url": {"type": str, "required": False},
                "cover_image_url": {"type": str, "required": False},
                "spl_hash": {"type": str, "required": False},
                "pool_name": {"type": str, "required": False},
                "is_devnet": {"type": bool, "required": False},
                "with_pool": {"type": bool, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)

           
            
            transaction = await self.solana_kit.create_3land_nft(
                item_name=data["item_name"],
                seller_fee=data["seller_fee"],
                item_amount=data["item_amount"],
                item_symbol=data["item_symbol"],
                item_description=data["item_description"],
                traits=data["traits"],
                price=data.get("price"),
                main_image_url=data.get("main_image_url"),
                cover_image_url=data.get("cover_image_url"),
                spl_hash=data.get("spl_hash"),
                pool_name=data.get("pool_name"),
                is_devnet=data.get("is_devnet", False),
                with_pool=data.get("with_pool", False),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error creating 3land NFT: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")


def get_land_tools(solana_kit: SolanaAgentKit):
    return [
        Create3LandCollectionTool(solana_kit=solana_kit),
        Create3LandNFTTool(solana_kit=solana_kit)
    ]


