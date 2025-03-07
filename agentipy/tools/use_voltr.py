import logging
from decimal import Decimal
from typing import Any, Dict, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class VoltrManager:
    """
    Manager class to handle Voltr functionalities such as deposit, withdrawal, and fetching position values.
    """

    @staticmethod
    def deposit_strategy(
        agent: SolanaAgentKit,
        deposit_amount: str,
        vault: str,
        strategy: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Deposits funds into a Voltr strategy.

        :param agent: An instance of SolanaAgentKit.
        :param deposit_amount: Amount to deposit.
        :param vault: Vault address.
        :param strategy: Strategy address.
        :return: Transaction signature or error details.
        """
        try:
            if Decimal(deposit_amount) <= 0:
                raise ValueError("Deposit amount must be greater than zero.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "depositAmount": deposit_amount,
                "vault": vault,
                "strategy": strategy,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/voltr/deposit-strategy",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Voltr deposit: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Voltr deposit: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def get_position_values(agent: SolanaAgentKit, vault: str) -> Optional[Dict[str, Any]]:
        """
        Fetches the position values of a given vault.

        :param agent: An instance of SolanaAgentKit.
        :param vault: Vault address.
        :return: Position values or error details.
        """
        try:
            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "vault": vault,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/voltr/get-position-values",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Voltr position value fetch: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Voltr position value fetch: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def withdraw_strategy(
        agent: SolanaAgentKit,
        withdraw_amount: str,
        vault: str,
        strategy: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Withdraws funds from a Voltr strategy.

        :param agent: An instance of SolanaAgentKit.
        :param withdraw_amount: Amount to withdraw.
        :param vault: Vault address.
        :param strategy: Strategy address.
        :return: Transaction signature or error details.
        """
        try:
            if Decimal(withdraw_amount) <= 0:
                raise ValueError("Withdraw amount must be greater than zero.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "withdrawAmount": withdraw_amount,
                "vault": vault,
                "strategy": strategy,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/voltr/withdraw-strategy",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Voltr withdrawal: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Voltr withdrawal: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
