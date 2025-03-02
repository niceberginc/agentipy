import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class BackpackGetAccountBalancesTool(BaseTool):
    name: str = "backpack_get_account_balances"
    description: str = """
    Fetches account balances using the BackpackManager.

    Input: None
    Output:
    {
        "balances": "dict, the account balances",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            balances = await self.solana_kit.get_account_balances()
            return {
                "balances": balances,
                "message": "Success"
            }
        except Exception as e:
            return {
                "balances": None,
                "message": f"Error fetching account balances: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetAccountSettingsTool(BaseTool):
    name: str = "backpack_get_account_settings"
    description: str = """
    Fetches account settings using the BackpackManager.

    Input: None
    Output:
    {
        "settings": "dict, the account settings",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            settings = await self.solana_kit.get_account_settings()
            return {
                "settings": settings,
                "message": "Success"
            }
        except Exception as e:
            return {
                "settings": None,
                "message": f"Error fetching account settings: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackUpdateAccountSettingsTool(BaseTool):
    name: str = "backpack_update_account_settings"
    description: str = """
    Updates account settings using the BackpackManager.

    Input: A JSON string with additional parameters for the account settings.
    Output:
    {
        "result": "dict, the result of the update",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.update_account_settings(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error updating account settings: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetAccountDepositsTool(BaseTool):
    name: str = "backpack_get_account_deposits"
    description: str = """
    Fetches account deposits using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "deposits": "dict, the account deposit data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "sub_account_id": {"type": int, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)

            sub_account_id = data.get("sub_account_id")
            deposits = await self.solana_kit.get_account_deposits(
                sub_account_id=sub_account_id
            )
            return {
                "deposits": deposits,
                "message": "Success"
            }
        except Exception as e:
            return {
                "deposits": None,
                "message": f"Error fetching account deposits: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
