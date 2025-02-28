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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
    
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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
    
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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class TradeUsingDriftPerpAccountTool(BaseTool):
    name: str = "trade_using_drift_perp_account"
    description: str = """
    Executes a trade using a Drift perpetual account.

    Input: A JSON string with:
    {
        "amount": "float, trade amount",
        "symbol": "string, market symbol",
        "action": "string, 'long' or 'short'",
        "trade_type": "string, 'market' or 'limit'",
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
                "amount": {"type": float, "required": True},
                "symbol": {"type": str, "required": True},
                "action": {"type": str, "required": True},
                "trade_type": {"type": str, "required": True},
                "price": {"type": float, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)
            transaction = await self.solana_kit.trade_using_drift_perp_account(
                amount=data["amount"],
                symbol=data["symbol"],
                action=data["action"],
                trade_type=data["trade_type"],
                price=data.get("price"),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error trading using Drift perp account: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

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

class GetAvailableDriftMarketsTool(BaseTool):
    name: str = "get_available_drift_markets"
    description: str = """
    Retrieves available markets on Drift.

    Input: None.
    Output:
    {
        "markets": "dict, list of available Drift markets",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            markets = await self.solana_kit.get_available_drift_markets()
            return {
                "markets": markets,
                "message": "Success"
            }
        except Exception as e:
            return {
                "markets": None,
                "message": f"Error fetching available Drift markets: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class StakeToDriftInsuranceFundTool(BaseTool):
    name: str = "stake_to_drift_insurance_fund"
    description: str = """
    Stakes funds into the Drift insurance fund.

    Input: A JSON string with:
    {
        "amount": "float, amount to stake",
        "symbol": "string, token symbol"
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
                "symbol": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)

            
            
            transaction = await self.solana_kit.stake_to_drift_insurance_fund(
                amount=data["amount"],
                symbol=data["symbol"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error staking to Drift insurance fund: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class RequestUnstakeFromDriftInsuranceFundTool(BaseTool):
    name: str = "request_unstake_from_drift_insurance_fund"
    description: str = """
    Requests unstaking from the Drift insurance fund.

    Input: A JSON string with:
    {
        "amount": "float, amount to unstake",
        "symbol": "string, token symbol"
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
                "symbol": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)

         
            transaction = await self.solana_kit.request_unstake_from_drift_insurance_fund(
                amount=data["amount"],
                symbol=data["symbol"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error requesting unstake from Drift insurance fund: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class UnstakeFromDriftInsuranceFundTool(BaseTool):
    name: str = "unstake_from_drift_insurance_fund"
    description: str = """
    Completes an unstaking request from the Drift insurance fund.

    Input: A JSON string with:
    {
        "symbol": "string, token symbol"
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
                "symbol": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)

           
            transaction = await self.solana_kit.unstake_from_drift_insurance_fund(
                symbol=data["symbol"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error unstaking from Drift insurance fund: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class DriftSwapSpotTokenTool(BaseTool):
    name: str = "drift_swap_spot_token"
    description: str = """
    Swaps spot tokens on Drift.

    Input: A JSON string with:
    {
        "from_symbol": "string, token to swap from",
        "to_symbol": "string, token to swap to",
        "slippage": "float, optional, allowed slippage",
        "to_amount": "float, optional, desired amount of the output token",
        "from_amount": "float, optional, amount of the input token"
    }
    Output:
    {
        "transaction": "dict, swap transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "from_symbol": {"type": str, "required": True},
                "to_symbol": {"type": str, "required": True},
                "slippage": {"type": float, "required": False},
                "to_amount": {"type": float, "required": False},
                "from_amount": {"type": float, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)           
            transaction = await self.solana_kit.drift_swap_spot_token(
                from_symbol=data["from_symbol"],
                to_symbol=data["to_symbol"],
                slippage=data.get("slippage"),
                to_amount=data.get("to_amount"),
                from_amount=data.get("from_amount"),
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error swapping spot token on Drift: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class GetDriftPerpMarketFundingRateTool(BaseTool):
    name: str = "get_drift_perp_market_funding_rate"
    description: str = """
    Retrieves the funding rate for a Drift perpetual market.

    Input: A JSON string with:
    {
        "symbol": "string, market symbol (must end in '-PERP')",
        "period": "string, optional, funding rate period, either 'year' or 'hour' (default: 'year')"
    }
    Output:
    {
        "funding_rate": "dict, funding rate details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "symbol": {"type": str, "required": True},
                "period": {"type": str, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)            
            funding_rate = await self.solana_kit.get_drift_perp_market_funding_rate(
                symbol=data["symbol"],
                period=data.get("period", "year"),
            )
            return {
                "funding_rate": funding_rate,
                "message": "Success"
            }
        except Exception as e:
            return {
                "funding_rate": None,
                "message": f"Error getting Drift perp market funding rate: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class GetDriftEntryQuoteOfPerpTradeTool(BaseTool):
    name: str = "get_drift_entry_quote_of_perp_trade"
    description: str = """
    Retrieves the entry quote for a perpetual trade on Drift.

    Input: A JSON string with:
    {
        "amount": "float, trade amount",
        "symbol": "string, market symbol (must end in '-PERP')",
        "action": "string, 'long' or 'short'"
    }
    Output:
    {
        "entry_quote": "dict, entry quote details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "amount": {"type": float, "required": True},
                "symbol": {"type": str, "required": True},
                "action": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            entry_quote = await self.solana_kit.get_drift_entry_quote_of_perp_trade(
                amount=data["amount"],
                symbol=data["symbol"],
                action=data["action"],
            )
            return {
                "entry_quote": entry_quote,
                "message": "Success"
            }
        except Exception as e:
            return {
                "entry_quote": None,
                "message": f"Error getting Drift entry quote of perp trade: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


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
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


def get_driftvault_tools(solana_kit: SolanaAgentKit):
    return [
        GetDriftLendBorrowApyTool(solana_kit=solana_kit),
        CreateDriftVaultTool(solana_kit=solana_kit),
        UpdateDriftVaultDelegateTool(solana_kit=solana_kit),
        UpdateDriftVaultTool(solana_kit=solana_kit),
        GetDriftVaultInfoTool(solana_kit=solana_kit),
        DepositIntoDriftVaultTool(solana_kit=solana_kit),
        RequestWithdrawalFromDriftVaultTool(solana_kit=solana_kit),
        WithdrawFromDriftVaultTool(solana_kit=solana_kit),
        DeriveDriftVaultAddressTool(solana_kit=solana_kit),
        CreateDriftUserAccountTool(solana_kit=solana_kit),
        DepositToDriftUserAccountTool(solana_kit=solana_kit),
        WithdrawFromDriftUserAccountTool(solana_kit=solana_kit),
        TradeUsingDriftPerpAccountTool(solana_kit=solana_kit),
        CheckIfDriftAccountExistsTool(solana_kit=solana_kit),
        DriftUserAccountInfoTool(solana_kit=solana_kit),
        GetAvailableDriftMarketsTool(solana_kit=solana_kit),
        StakeToDriftInsuranceFundTool(solana_kit=solana_kit),
        RequestUnstakeFromDriftInsuranceFundTool(solana_kit=solana_kit),
        UnstakeFromDriftInsuranceFundTool(solana_kit=solana_kit),
        DriftSwapSpotTokenTool(solana_kit=solana_kit),
        GetDriftPerpMarketFundingRateTool(solana_kit=solana_kit),
        GetDriftEntryQuoteOfPerpTradeTool(solana_kit=solana_kit),
        TradeUsingDelegatedDriftVaultTool(solana_kit=solana_kit)
        
    ]
