import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaFaucetTool(BaseTool):
    name:str = "solana_request_funds"
    description:str = "Request test funds from a Solana faucet."
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            result = await self.solana_kit.request_faucet_funds()
            return {
                "status": "success",
                "message": "Faucet funds requested successfully",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }

    def _run(self):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
