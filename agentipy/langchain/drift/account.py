import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class CreateDriftUserAccountTool(BaseTool):
    name: str = "create_drift_user_account"
    description: str = """
    Creates a Drift user account with an initial deposit.

    Input: A JSON string with:
    {
        "deposit_amount": "float, amount to deposit",
        "deposit_symbol": "string, symbol of the asset to deposit"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "deposit_amount": {"type": float, "required": True},
                "deposit_symbol": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            transaction = await self.solana_kit.create_drift_user_account(
                deposit_amount=data["deposit_amount"],
                deposit_symbol=data["deposit_symbol"],
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error creating Drift user account: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class DepositToDriftUserAccountTool(BaseTool):
    name: str = "deposit_to_drift_user_account"
    description: str = """
    Deposits funds into a Drift user account.

    Input: A JSON string with:
    {
        "amount": "float, amount to deposit",
        "symbol": "string, symbol of the asset",
        "is_repayment": "bool, optional, whether the deposit is a loan repayment"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "amount": {"type": float, "required": True},
                "symbol": {"type": str, "required": True},
                "is_repayment": {"type": bool, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            transaction = await self.solana_kit.deposit_to_drift_user_account(
                amount=data["amount"],
                symbol=data["symbol"],
                is_repayment=data.get("is_repayment"),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error depositing to Drift user account: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")
    
class WithdrawFromDriftUserAccountTool(BaseTool):
    name: str = "withdraw_from_drift_user_account"
    description: str = """
    Withdraws funds from a Drift user account.

    Input: A JSON string with:
    {
        "amount": "float, amount to withdraw",
        "symbol": "string, symbol of the asset",
        "is_borrow": "bool, optional, whether the withdrawal is a borrow request"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "amount": {"type": float, "required": True},
                "symbol": {"type": str, "required": True},
                "is_borrow": {"type": bool, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)
          
            transaction = await self.solana_kit.withdraw_from_drift_user_account(
                amount=data["amount"],
                symbol=data["symbol"],
                is_borrow=data.get("is_borrow"),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error withdrawing from Drift user account: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class CheckIfDriftAccountExistsTool(BaseTool):
    name: str = "check_if_drift_account_exists"
    description: str = """
    Checks if a Drift user account exists.

    Input: None.
    Output:
    {
        "exists": "bool, whether the Drift user account exists",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            exists = await self.solana_kit.check_if_drift_account_exists()
            return {
                "exists": exists,
                "message": "Success"
            }
        except Exception as e:
            return {
                "exists": None,
                "message": f"Error checking Drift account existence: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class DriftUserAccountInfoTool(BaseTool):
    name: str = "drift_user_account_info"
    description: str = """
    Retrieves Drift user account information.

    Input: None.
    Output:
    {
        "account_info": "dict, account details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            account_info = await self.solana_kit.drift_user_account_info()
            return {
                "account_info": account_info,
                "message": "Success"
            }
        except Exception as e:
            return {
                "account_info": None,
                "message": f"Error fetching Drift user account info: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

