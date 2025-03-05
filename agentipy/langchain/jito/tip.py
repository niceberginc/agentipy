from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit

class SolanaGetTipAccounts(BaseTool):
    name: str = "get_tip_accounts"
    description: str = """
    Get all available Jito tip accounts.

    Output:
    {
        "accounts": "List of Jito tip accounts"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            result = await self.solana_kit.get_tip_accounts()
            return {
                "accounts": result
            }
        except Exception as e:
            return {
                "accounts": None
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaGetRandomTipAccount(BaseTool):
    name: str = "get_random_tip_account"
    description: str = """
    Get a randomly selected Jito tip account from the existing list.

    Output:
    {
        "account": "Randomly selected Jito tip account"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            result = await self.solana_kit.get_random_tip_account()
            return {
                "account": result
            }
        except Exception as e:
            return {
                "account": None
            }

    def _run(self):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
