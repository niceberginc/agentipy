import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class BackpackGetOpenPositionsTool(BaseTool):
    name: str = "backpack_get_open_positions"
    description: str = """
    Fetches open positions using the BackpackManager.

    Input: None
    Output:
    {
        "open_positions": "list, the open positions",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            open_positions = await self.solana_kit.get_open_positions()
            return {
                "open_positions": open_positions,
                "message": "Success"
            }
        except Exception as e:
            return {
                "open_positions": None,
                "message": f"Error fetching open positions: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetBorrowLendPositionsTool(BaseTool):
    name: str = "backpack_get_borrow_lend_positions"
    description: str = """
    Fetches borrow/lend positions using the BackpackManager.

    Input: None
    Output:
    {
        "positions": "list, the borrow/lend positions",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            positions = await self.solana_kit.get_borrow_lend_positions()
            return {
                "positions": positions,
                "message": "Success"
            }
        except Exception as e:
            return {
                "positions": None,
                "message": f"Error fetching borrow/lend positions: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackExecuteBorrowLendTool(BaseTool):
    name: str = "backpack_execute_borrow_lend"
    description: str = """
    Executes a borrow/lend operation using the BackpackManager.

    Input: A JSON string with:
    {
        "quantity": "string, the amount to borrow or lend",
        "side": "string, either 'borrow' or 'lend'",
        "symbol": "string, the token symbol"
    }
    Output:
    {
        "result": "dict, the result of the operation",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "quantity": {"type": str, "required": True},
                "side": {"type": str, "required": True},
                "symbol": {"type": str, "required": True}
            }
            validate_input(data, schema)

            result = await self.solana_kit.execute_borrow_lend(
                quantity=data["quantity"],
                side=data["side"],
                symbol=data["symbol"]
            )
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error executing borrow/lend operation: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetBorrowHistoryTool(BaseTool):
    name: str = "backpack_get_borrow_history"
    description: str = """
    Fetches borrow history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "borrow_history": "list, the borrow history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            borrow_history = await self.solana_kit.get_borrow_history(**data)
            return {
                "borrow_history": borrow_history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "borrow_history": None,
                "message": f"Error fetching borrow history: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetInterestHistoryTool(BaseTool):
    name: str = "backpack_get_interest_history"
    description: str = """
    Fetches interest history using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "interest_history": "list, the interest history records",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            interest_history = await self.solana_kit.get_interest_history(**data)
            return {
                "interest_history": interest_history,
                "message": "Success"
            }
        except Exception as e:
            return {
                "interest_history": None,
                "message": f"Error fetching interest history: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
