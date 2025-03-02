import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class BackpackGetFillHistoryTool(BaseTool):
    name: str = "backpack_get_fill_history"
    description: str = """
    Fetches the fill history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the fill history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_fill_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching fill history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetBorrowPositionHistoryTool(BaseTool):
    name: str = "backpack_get_borrow_position_history"
    description: str = """
    Fetches the borrow position history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the borrow position history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_borrow_position_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching borrow position history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetFundingPaymentsTool(BaseTool):
    name: str = "backpack_get_funding_payments"
    description: str = """
    Fetches funding payments using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "payments": "list, the funding payments records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            payments = await self.solana_kit.get_funding_payments(**data)
            return {
                "payments": payments,
                "message": "Success"
            }
        except Exception as e:
            return {
                "payments": None,
                "message": f"Error fetching funding payments: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetOrderHistoryTool(BaseTool):
    name: str = "backpack_get_order_history"
    description: str = """
    Fetches order history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the order history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_order_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching order history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetPnlHistoryTool(BaseTool):
    name: str = "backpack_get_pnl_history"
    description: str = """
    Fetches PNL history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the PNL history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_pnl_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching PNL history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetSettlementHistoryTool(BaseTool):
    name: str = "backpack_get_settlement_history"
    description: str = """
    Fetches settlement history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "history": "list, the settlement history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            history = await self.solana_kit.get_settlement_history(**data)
            return {
                "history": history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "history": None,
                "message": f"Error fetching settlement history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
