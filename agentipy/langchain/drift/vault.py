import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class GetDriftLendBorrowApyTool(BaseTool):
    name: str = "get_drift_lend_borrow_apy"
    description: str = """
    Retrieves the lending and borrowing APY for a given symbol on Drift.

    Input: A JSON string with:
    {
        "symbol": "string, token symbol"
    }
    Output:
    {
        "apy_data": "dict, lending and borrowing APY details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "symbol": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
               
            apy_data = await self.solana_kit.get_drift_lend_borrow_apy(
                symbol=data["symbol"]
            )
            return {
                "apy_data": apy_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "apy_data": None,
                "message": f"Error getting Drift lend/borrow APY: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class CreateDriftVaultTool(BaseTool):
    name: str = "create_drift_vault"
    description: str = """
    Creates a Drift vault.

    Input: A JSON string with:
    {
        "name": "string, vault name",
        "market_name": "string, market name format '<name>-<name>'",
        "redeem_period": "int, redeem period in blocks",
        "max_tokens": "int, maximum number of tokens",
        "min_deposit_amount": "float, minimum deposit amount",
        "management_fee": "float, management fee percentage",
        "profit_share": "float, profit share percentage",
        "hurdle_rate": "float, optional, hurdle rate",
        "permissioned": "bool, optional, whether the vault is permissioned"
    }
    Output:
    {
        "vault_details": "dict, vault creation details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "name": {"type": str, "required": True},
                "market_name": {"type": str, "required": True},
                "redeem_period": {"type": int, "required": True},
                "max_tokens": {"type": int, "required": True},
                "min_deposit_amount": {"type": float, "required": True},
                "management_fee": {"type": float, "required": True},
                "profit_share": {"type": float, "required": True},
                "hurdle_rate": {"type": float, "required": False},
                "permissioned": {"type": bool, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            vault_details = await self.solana_kit.create_drift_vault(
                name=data["name"],
                market_name=data["market_name"],
                redeem_period=data["redeem_period"],
                max_tokens=data["max_tokens"],
                min_deposit_amount=data["min_deposit_amount"],
                management_fee=data["management_fee"],
                profit_share=data["profit_share"],
                hurdle_rate=data.get("hurdle_rate"),
                permissioned=data.get("permissioned"),
            )
            return {
                "vault_details": vault_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "vault_details": None,
                "message": f"Error creating Drift vault: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class UpdateDriftVaultDelegateTool(BaseTool):
    name: str = "update_drift_vault_delegate"
    description: str = """
    Updates the delegate address for a Drift vault.

    Input: A JSON string with:
    {
        "vault": "string, vault address",
        "delegate_address": "string, new delegate address"
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
                "vault": {"type": str, "required": True},
                "delegate_address": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            transaction = await self.solana_kit.update_drift_vault_delegate(
                vault=data["vault"],
                delegate_address=data["delegate_address"],
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error updating Drift vault delegate: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class UpdateDriftVaultTool(BaseTool):
    name: str = "update_drift_vault"
    description: str = """
    Updates an existing Drift vault.

    Input: A JSON string with:
    {
        "vault_address": "string, address of the vault",
        "name": "string, vault name",
        "market_name": "string, market name format '<name>-<name>'",
        "redeem_period": "int, redeem period in blocks",
        "max_tokens": "int, maximum number of tokens",
        "min_deposit_amount": "float, minimum deposit amount",
        "management_fee": "float, management fee percentage",
        "profit_share": "float, profit share percentage",
        "hurdle_rate": "float, optional, hurdle rate",
        "permissioned": "bool, optional, whether the vault is permissioned"
    }
    Output:
    {
        "vault_update": "dict, vault update details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "vault_address": {"type": str, "required": True},
                "name": {"type": str, "required": True},
                "market_name": {"type": str, "required": True},
                "redeem_period": {"type": int, "required": True},
                "max_tokens": {"type": int, "required": True},
                "min_deposit_amount": {"type": float, "required": True},
                "management_fee": {"type": float, "required": True},
                "profit_share": {"type": float, "required": True},
                "hurdle_rate": {"type": float, "required": False},
                "permissioned": {"type": bool, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            vault_update = await self.solana_kit.update_drift_vault(
                vault_address=data["vault_address"],
                name=data["name"],
                market_name=data["market_name"],
                redeem_period=data["redeem_period"],
                max_tokens=data["max_tokens"],
                min_deposit_amount=data["min_deposit_amount"],
                management_fee=data["management_fee"],
                profit_share=data["profit_share"],
                hurdle_rate=data.get("hurdle_rate"),
                permissioned=data.get("permissioned"),
            )
            return {
                "vault_update": vault_update,
                "message": "Success"
            }
        except Exception as e:
            return {
                "vault_update": None,
                "message": f"Error updating Drift vault: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class GetDriftVaultInfoTool(BaseTool):
    name: str = "get_drift_vault_info"
    description: str = """
    Retrieves information about a specific Drift vault.

    Input: A JSON string with:
    {
        "vault_name": "string, name of the vault"
    }
    Output:
    {
        "vault_info": "dict, vault details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "vault_name": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            vault_info = await self.solana_kit.get_drift_vault_info(
                vault_name=data["vault_name"]
            )
            return {
                "vault_info": vault_info,
                "message": "Success"
            }
        except Exception as e:
            return {
                "vault_info": None,
                "message": f"Error retrieving Drift vault info: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class DepositIntoDriftVaultTool(BaseTool):
    name: str = "deposit_into_drift_vault"
    description: str = """
    Deposits funds into a Drift vault.

    Input: A JSON string with:
    {
        "amount": "float, amount to deposit",
        "vault": "string, vault address"
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
                "vault": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            transaction = await self.solana_kit.deposit_into_drift_vault(
                amount=data["amount"],
                vault=data["vault"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error depositing into Drift vault: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class RequestWithdrawalFromDriftVaultTool(BaseTool):
    name: str = "request_withdrawal_from_drift_vault"
    description: str = """
    Requests a withdrawal from a Drift vault.

    Input: A JSON string with:
    {
        "amount": "float, amount to withdraw",
        "vault": "string, vault address"
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
                "vault": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            transaction = await self.solana_kit.request_withdrawal_from_drift_vault(
                amount=data["amount"],
                vault=data["vault"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error requesting withdrawal from Drift vault: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class WithdrawFromDriftVaultTool(BaseTool):
    name: str = "withdraw_from_drift_vault"
    description: str = """
    Withdraws funds from a Drift vault after a withdrawal request.

    Input: A JSON string with:
    {
        "vault": "string, vault address"
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
                "vault": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            transaction = await self.solana_kit.withdraw_from_drift_vault(
                vault=data["vault"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error withdrawing from Drift vault: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class DeriveDriftVaultAddressTool(BaseTool):
    name: str = "derive_drift_vault_address"
    description: str = """
    Derives the Drift vault address from a given name.

    Input: A JSON string with:
    {
        "name": "string, vault name"
    }
    Output:
    {
        "vault_address": "string, derived vault address",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "name": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            vault_address = await self.solana_kit.derive_drift_vault_address(
                name=data["name"]
            )
            return {
                "vault_address": vault_address,
                "message": "Success"
            }
        except Exception as e:
            return {
                "vault_address": None,
                "message": f"Error deriving Drift vault address: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class TradeUsingDelegatedDriftVaultTool(BaseTool):
    name: str = "trade_using_delegated_drift_vault"
    description: str = """
    Executes a trade using a delegated Drift vault.

    Input: A JSON string with:
    {
        "vault": "string, vault address",
        "amount": "float, trade amount",
        "symbol": "string, market symbol",
        "action": "string, either 'long' or 'short'",
        "trade_type": "string, either 'market' or 'limit'",
        "price": "float, optional, trade execution price"
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
                "vault": {"type": str, "required": True},
                "amount": {"type": float, "required": True},
                "symbol": {"type": str, "required": True},
                "action": {"type": str, "required": True},
                "trade_type": {"type": str, "required": True},
                "price": {"type": float, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            transaction = await self.solana_kit.trade_using_delegated_drift_vault(
                vault=data["vault"],
                amount=data["amount"],
                symbol=data["symbol"],
                action=data["action"],
                trade_type=data["trade_type"],
                price=data.get("price")
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error trading using delegated Drift vault: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

