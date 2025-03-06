import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input

class SolanaMintMetaplexCoreNFTTool(BaseTool):
    name: str = "solana_mint_metaplex_core_nft"
    description: str = """
    Mints an NFT using the Metaplex Core program.

    Input: A JSON string with:
    {
        "collection_mint": "string, the collection mint's public key",
        "name": "string, the name of the NFT",
        "uri": "string, the metadata URI",
        "seller_fee_basis_points": "int, royalty in basis points",
        "address": "string, the creator's public key",
        "share": "string, share percentage for the creator",
        "recipient": "string, recipient's public key"
    }

    Output:
    {
        "success": "bool, whether the operation was successful",
        "transaction": "string, the transaction signature if successful",
        "message": "string, additional details or error information"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "collection_mint": {"type": str, "required": True},
                "name": {"type": str, "required": True},
                "uri": {"type": str, "required": True},
                "seller_fee_basis_points": {"type": int, "required": True, "min": 0, "max": 10000},
                "address": {"type": str, "required": True},
                "share": {"type": str, "required": True},
                "recipient": {"type": str, "required": True}
            }
            validate_input(data, schema)

            collection_mint = data["collection_mint"]
            name = data["name"]
            uri = data["uri"]
            seller_fee_basis_points = data["seller_fee_basis_points"]
            address = data["address"]
            share = data["share"]
            recipient = data["recipient"]

            result = await self.solana_kit.mint_metaplex_core_nft(
                collectionMint=collection_mint,
                name=name,
                uri=uri,
                sellerFeeBasisPoints=seller_fee_basis_points,
                address=address,
                share=share,
                recipient=recipient,
            )
            return result
        except Exception as e:
            return {"success": False, "message": f"Error minting NFT: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
