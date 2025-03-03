import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit

class SolanaBurnAndCloseTool(BaseTool):
    name: str = "solana_burn_and_close_account"
    description: str = """
    Burn and close a single Solana token account.

    Input: A JSON string with:
    {
        "token_account": "public_key_of_the_token_account"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            required_fields = ["token_account"]
            data = json.loads(input)

            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            if not isinstance(data["token_account"], str):
                raise ValueError("Token account must be a string")
            
            token_account = data["token_account"]


            result = await self.solana_kit.burn_and_close_accounts(token_account)

            return {
                "status": "success",
                "message": "Token account burned and closed successfully.",
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "code": getattr(e, "code", "UNKNOWN_ERROR"),
            }
        
    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
