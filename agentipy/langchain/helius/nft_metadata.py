import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaHeliusGetNFTMetadataTool(BaseTool):
    name: str = "solana_helius_get_nft_metadata"
    description: str = """
    Fetch metadata for NFTs based on their mint accounts.

    Input: A JSON string with:
    {
        "mint_addresses": ["string, the mint addresses of the NFTs"]
    }

    Output:
    {
        "metadata": "list of NFT metadata"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "mint_addresses": {"type": list, "required": True}
            }
            validate_input(data, schema)
            mint_addresses = data["mint_addresses"]

            result = await self.solana_kit.get_nft_metadata(mint_addresses)
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
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

