import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class BackpackGetOpenOrdersTool(BaseTool):
    name: str = "backpack_get_open_orders"
    description: str = """
    Fetches open orders using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "open_orders": "list, the open orders",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            open_orders = await self.solana_kit.get_open_orders(**data)
            return {
                "open_orders": open_orders,
                "message": "Success"
            }
        except Exception as e:
            return {
                "open_orders": None,
                "message": f"Error fetching open orders: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackExecuteOrderTool(BaseTool):
    name: str = "backpack_execute_order"
    description: str = """
    Executes an order using the BackpackManager.

    Input: A JSON string with order parameters.
    Output:
    {
        "result": "dict, the execution result",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.execute_order(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error executing order: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackCancelOpenOrderTool(BaseTool):
    name: str = "backpack_cancel_open_order"
    description: str = """
    Cancels an open order using the BackpackManager.

    Input: A JSON string with order details.
    Output:
    {
        "result": "dict, the cancellation result",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.cancel_open_order(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error canceling open order: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackCancelOpenOrdersTool(BaseTool):
    name: str = "backpack_cancel_open_orders"
    description: str = """
    Cancels multiple open orders using the BackpackManager.

    Input: A JSON string with order details.
    Output:
    {
        "result": "dict, the cancellation result",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            result = await self.solana_kit.cancel_open_orders(**data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error canceling open orders: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetUsersOpenOrdersTool(BaseTool):
    name: str = "backpack_get_users_open_orders"
    description: str = """
    Fetches user's open orders using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "open_orders": "list, the user's open orders",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            open_orders = await self.solana_kit.get_users_open_orders(**data)
            return {
                "open_orders": open_orders,
                "message": "Success"
            }
        except Exception as e:
            return {
                "open_orders": None,
                "message": f"Error fetching user's open orders: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
