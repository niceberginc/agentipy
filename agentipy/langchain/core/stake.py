from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit


class SolanaStakeTool(BaseTool):
    name:str = "solana_stake"
    description:str = "Stake assets on Solana. Input is the amount to stake."
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            amount = int(input)
            result = await self.solana_kit.stake(amount)
            return {
                "status": "success",
                "message": "Assets staked successfully",
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

