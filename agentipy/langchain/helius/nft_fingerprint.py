import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaHeliusGetNFTFingerprintTool(BaseTool):
    name: str = "solana_helius_get_nft_fingerprint"
    description: str = """
    Fetch NFT fingerprint for a list of mint addresses.

    Input: A JSON string with:
    {
        "mints": ["string, the mint addresses of the NFTs"]
    }

    Output:
    {
        "fingerprint": "list of NFT fingerprint data"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:    
            data = json.loads(input)
            schema = {
                "mints": {"type": list, "required": True}
            }
            validate_input(data, schema)
            mints = data["mints"]

            result = await self.solana_kit.get_nft_fingerprint(mints)
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
