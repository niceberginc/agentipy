import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class TensorListNFTForSaleTool(BaseTool):
    name: str = "tensor_list_nft_for_sale"
    description: str = """
    Lists an NFT for sale on Tensor.

    Input: A JSON string with:
    {
        "price": "float, the sale price of the NFT",
        "nft_mint": "string, the NFT mint address"
    }

    Output:
    {
        "transaction_details": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "price": {"type": float, "required": True},
                "nft_mint": {"type": str, "required": True},
            }
            validate_input(data, schema)

            price = data["price"]
            nft_mint = data["nft_mint"]

            result = await self.solana_kit.list_nft_for_sale(price, nft_mint)
            return {
                "status": "success",
                "transaction_details": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


class TensorCancelListingTool(BaseTool):
    name: str = "tensor_cancel_listing"
    description: str = """
    Cancels an NFT listing on Tensor.

    Input: A JSON string with:
    {
        "nft_mint": "string, the NFT mint address"
    }

    Output:
    {
        "transaction_details": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "nft_mint": {"type": str, "required": True},
            }
            validate_input(data, schema)

            nft_mint = data["nft_mint"]

            result = await self.solana_kit.cancel_listing(nft_mint)
            return {
                "status": "success",
                "transaction_details": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
