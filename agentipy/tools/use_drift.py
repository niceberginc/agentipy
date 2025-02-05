import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class DriftManager:
    @staticmethod
    def create_drift_user_account(
        agent: SolanaAgentKit,
        deposit_amount: float,
        deposit_symbol: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a Drift user account and deposits initial funds.
        """
        try:
            if not all([deposit_amount, deposit_symbol]):
                raise ValueError("Deposit amount and deposit symbol are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "depositAmount": deposit_amount,
                "depositSymbol": deposit_symbol,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/create-drift-user-account",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}
        
        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Drift user account creation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Drift user account creation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def deposit_to_drift_user_account(
        agent: SolanaAgentKit,
        amount: float,
        symbol: str,
        is_repayment: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Deposits funds into a Drift user account.
        """
        try:
            if not all([amount, symbol]):
                raise ValueError("Amount and symbol are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "amount": amount,
                "symbol": symbol,
                "isRepayment": is_repayment,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/deposit-to-drift-user-account",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}
        
        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Drift deposit: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Drift deposit: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def withdraw_from_drift_user_account(
        agent: SolanaAgentKit,
        amount: float,
        symbol: str,
        is_borrow: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Withdraws funds from a Drift user account.
        """
        try:
            if not all([amount, symbol]):
                raise ValueError("Amount and symbol are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "amount": amount,
                "symbol": symbol,
                "isBorrow": is_borrow,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/withdraw-from-drift-user-account",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}
        
        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Drift withdrawal: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Drift withdrawal: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def trade_using_drift_perp_account(
        agent: SolanaAgentKit,
        amount: float,
        symbol: str,
        action: str,
        trade_type: str,
        price: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Executes a trade using a Drift perpetual account.
        """
        try:
            if not all([amount, symbol, action, trade_type]):
                raise ValueError("Amount, symbol, action, and trade type are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "amount": amount,
                "symbol": symbol,
                "action": action,
                "type": trade_type,
                "price": price,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/trade-using-drift-perp-account",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}
        
        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Drift perpetual trade: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Drift perpetual trade: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def check_if_drift_account_exists(
        agent: SolanaAgentKit,
    ) -> Optional[Dict[str, Any]]:
        """
        Checks if the user has an existing Drift account.
        """
        try:
            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/check-if-drift-account-exists",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "value": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while checking Drift account: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error while checking Drift account: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def drift_user_account_info(
        agent: SolanaAgentKit,
    ) -> Optional[Dict[str, Any]]:
        """
        Fetches the user's Drift account information.
        """
        try:
            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/drift-user-account-info",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "value": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while fetching Drift account info: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error while fetching Drift account info: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def get_available_drift_markets(
        agent: SolanaAgentKit,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves available Drift markets.
        """
        try:
            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/get-available-drift-markets",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "value": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while fetching Drift markets: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error while fetching Drift markets: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def stake_to_drift_insurance_fund(
        agent: SolanaAgentKit,
        amount: float,
        symbol: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Stakes funds to the Drift insurance fund.
        """
        try:
            if not all([amount, symbol]):
                raise ValueError("Amount and symbol are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "amount": amount,
                "symbol": symbol,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/stake-to-drift-insurance-fund",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while staking to Drift insurance fund: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while staking to Drift insurance fund: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
    
    @staticmethod
    def request_unstake_from_drift_insurance_fund(
        agent: SolanaAgentKit,
        amount: float,
        symbol: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Requests an unstake from the Drift insurance fund.
        """
        try:
            if not all([amount, symbol]):
                raise ValueError("Amount and symbol are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "amount": amount,
                "symbol": symbol,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/request-unstake-from-drift-insurance-fund",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while requesting unstake: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while requesting unstake: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def unstake_from_drift_insurance_fund(
        agent: SolanaAgentKit,
        symbol: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Unstakes from the Drift insurance fund.
        """
        try:
            if not symbol:
                raise ValueError("Symbol is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "symbol": symbol,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/unstake-from-drift-insurance-fund",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while unstaking: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while unstaking: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def drift_swap_spot_token(
        agent: SolanaAgentKit,
        from_symbol: str,
        to_symbol: str,
        slippage: Optional[float] = None,
        to_amount: Optional[float] = None,
        from_amount: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Swaps a spot token on Drift.
        """
        try:
            if not all([from_symbol, to_symbol]):
                raise ValueError("From symbol and to symbol are required.")

            if (to_amount is None and from_amount is None) or (to_amount is not None and from_amount is not None):
                raise ValueError("Provide either 'from_amount' or 'to_amount', but not both.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            swap_params = {
                "fromSymbol": from_symbol,
                "toSymbol": to_symbol,
                "slippage": slippage,
                **({"toAmount": to_amount} if to_amount is not None else {"fromAmount": from_amount}),
            }

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                **swap_params,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/drift-swap-spot-token",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while swapping spot token: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while swapping spot token: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def get_drift_perp_market_funding_rate(
        agent: SolanaAgentKit,
        symbol: str,
        period: str = "year",
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves the funding rate for a Drift perpetual market.
        """
        try:
            if not symbol.endswith("-PERP"):
                raise ValueError("Symbol must be in the format '<name>-PERP'.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "symbol": symbol,
                "period": period,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/get-drift-perp-market-funding-rate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "value": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while retrieving funding rate: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while retrieving funding rate: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def get_drift_entry_quote_of_perp_trade(
        agent: SolanaAgentKit,
        amount: float,
        symbol: str,
        action: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves the entry quote for a Drift perpetual trade.
        """
        try:
            if not all([amount, symbol, action]):
                raise ValueError("Amount, symbol, and action are required.")

            if not symbol.endswith("-PERP"):
                raise ValueError("Symbol must be in the format '<name>-PERP'.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "amount": amount,
                "symbol": symbol,
                "action": action,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/get-drift-entry-quote-of-perp-trade",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "value": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while retrieving entry quote: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while retrieving entry quote: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def get_drift_lend_borrow_apy(
        agent: SolanaAgentKit,
        symbol: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves the lending and borrowing APY for a Drift market.
        """
        try:
            if not symbol:
                raise ValueError("Symbol is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "symbol": symbol,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/get-drift-lend-borrow-apy",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "value": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while retrieving APY: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while retrieving APY: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def create_drift_vault(
        agent: SolanaAgentKit,
        name: str,
        market_name: str,
        redeem_period: int,
        max_tokens: int,
        min_deposit_amount: float,
        management_fee: float,
        profit_share: float,
        hurdle_rate: Optional[float] = None,
        permissioned: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a Drift vault.
        """
        try:
            if not all([name, market_name, redeem_period, max_tokens, min_deposit_amount, management_fee, profit_share]):
                raise ValueError("All vault parameters are required.")

            if not "-" in market_name:
                raise ValueError("Market name must be in the format '<name>-<name>'.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            vault_params = {
                "name": name,
                "marketName": market_name,
                "redeemPeriod": redeem_period,
                "maxTokens": max_tokens,
                "minDepositAmount": min_deposit_amount,
                "managementFee": management_fee,
                "profitShare": profit_share,
                "hurdleRate": hurdle_rate,
                "permissioned": permissioned,
            }

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                **vault_params,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/create-drift-vault",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "value": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while creating Drift vault: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while creating Drift vault: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def update_drift_vault_delegate(
        agent: SolanaAgentKit,
        vault: str,
        delegate_address: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Updates the delegate for a Drift vault.
        """
        try:
            if not all([vault, delegate_address]):
                raise ValueError("Vault and delegate address are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "vault": vault,
                "delegateAddress": delegate_address,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/update-drift-vault-delegate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while updating vault delegate: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while updating vault delegate: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
        
    @staticmethod
    def update_drift_vault(
        agent: SolanaAgentKit,
        vault_address: str,
        name: str,
        market_name: str,
        redeem_period: int,
        max_tokens: int,
        min_deposit_amount: float,
        management_fee: float,
        profit_share: float,
        hurdle_rate: Optional[float] = None,
        permissioned: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Updates an existing Drift vault.
        """
        try:
            if not all([vault_address, name, market_name, redeem_period, max_tokens, min_deposit_amount, management_fee, profit_share]):
                raise ValueError("All vault parameters are required.")

            if "-" not in market_name:
                raise ValueError("Market name must be in the format '<name>-<name>'.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            vault_params = {
                "vaultAddress": vault_address,
                "name": name,
                "marketName": market_name,
                "redeemPeriod": redeem_period,
                "maxTokens": max_tokens,
                "minDepositAmount": min_deposit_amount,
                "managementFee": management_fee,
                "profitShare": profit_share,
                "hurdleRate": hurdle_rate,
                "permissioned": permissioned,
            }

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                **vault_params,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/update-drift-vault",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while updating Drift vault: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while updating Drift vault: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def get_drift_vault_info(
        agent: SolanaAgentKit,
        vault_name: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves information about a Drift vault.
        """
        try:
            if not vault_name:
                raise ValueError("Vault name is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "vaultName": vault_name,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/get-drift-vault-info",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "value": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while retrieving Drift vault info: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while retrieving Drift vault info: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def deposit_into_drift_vault(
        agent: SolanaAgentKit,
        amount: float,
        vault: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Deposits funds into a Drift vault.
        """
        try:
            if not all([amount, vault]):
                raise ValueError("Amount and vault address are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "amount": amount,
                "vault": vault,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/deposit-into-drift-vault",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while depositing into Drift vault: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while depositing into Drift vault: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def request_withdrawal_from_drift_vault(
        agent: SolanaAgentKit,
        amount: float,
        vault: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Requests a withdrawal from a Drift vault.
        """
        try:
            if not all([amount, vault]):
                raise ValueError("Amount and vault address are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "amount": amount,
                "vault": vault,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/request-withdrawal-from-drift-vault",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while requesting withdrawal from Drift vault: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while requesting withdrawal from Drift vault: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
        
    @staticmethod
    def withdraw_from_drift_vault(
        agent: SolanaAgentKit,
        vault: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Withdraws funds from a Drift vault.
        """
        try:
            if not vault:
                raise ValueError("Vault address is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "vault": vault,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/withdraw-from-drift-vault",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while withdrawing from Drift vault: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while withdrawing from Drift vault: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def derive_drift_vault_address(
        agent: SolanaAgentKit,
        name: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Derives a Drift vault address based on the vault name.
        """
        try:
            if not name:
                raise ValueError("Vault name is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "name": name,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/derive-drift-vault-address",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "value": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while deriving Drift vault address: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while deriving Drift vault address: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def trade_using_delegated_drift_vault(
        agent: SolanaAgentKit,
        vault: str,
        amount: float,
        symbol: str,
        action: str,
        trade_type: str,
        price: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Executes a trade using a delegated Drift vault.
        """
        try:
            if not all([vault, amount, symbol, action, trade_type]):
                raise ValueError("Vault, amount, symbol, action, and trade_type are required.")

            if action not in ["long", "short"]:
                raise ValueError("Invalid action. Must be 'long' or 'short'.")

            if trade_type not in ["market", "limit"]:
                raise ValueError("Invalid trade type. Must be 'market' or 'limit'.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            trade_params = {
                "vault": vault,
                "amount": amount,
                "symbol": symbol,
                "action": action,
                "type": trade_type,
                "price": price,
            }

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                **trade_params,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/drift/trade-using-delegated-drift-vault",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error while executing trade using delegated Drift vault: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error while executing trade using delegated Drift vault: {error}", exc_info=True)
            return {"success": False, "error": str(error)}