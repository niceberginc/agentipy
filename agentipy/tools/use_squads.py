import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)


class SquadsManager:
    """
    Manager class to handle Squads Protocol functionalities such as approving proposals,
    creating multisigs, creating proposals, and depositing to treasury.
    """

    @staticmethod
    def approve_multisig_proposal(
        agent: SolanaAgentKit,
        transaction_index: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Approves a multisig proposal.

        :param agent: An instance of SolanaAgentKit.
        :param transaction_index: The index of the transaction to approve.
        :return: Transaction signature or error details.
        """
        try:
            if transaction_index < 0:
                raise ValueError("Invalid transaction index.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "transactionIndex": transaction_index,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/squads/multisig-approve-proposal",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during multisig proposal approval: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during multisig proposal approval: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def create_squads_multisig(
        agent: SolanaAgentKit,
        creator: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a Squads multisig.

        :param agent: An instance of SolanaAgentKit.
        :param creator: The public key of the multisig creator.
        :return: Transaction signature or error details.
        """
        try:

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "creator": creator,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/squads/create-squads-multisig",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except ValueError:
            logger.error("Invalid creator public key.", exc_info=True)
            return {"success": False, "error": "Invalid creator public key."}
        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during multisig creation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during multisig creation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def create_multisig_proposal(
        agent: SolanaAgentKit,
        transaction_index: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a multisig proposal.

        :param agent: An instance of SolanaAgentKit.
        :param transaction_index: The index of the transaction to create a proposal for.
        :return: Transaction signature or error details.
        """
        try:
            if transaction_index < 0:
                raise ValueError("Invalid transaction index.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "transactionIndex": transaction_index,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/squads/multisig-create-proposal",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during multisig proposal creation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during multisig proposal creation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def deposit_to_multisig_treasury(
        agent: SolanaAgentKit,
        amount: float,
        vault_index: int,
        mint: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Deposits funds into the multisig treasury.

        :param agent: An instance of SolanaAgentKit.
        :param amount: The amount to deposit.
        :param vault_index: The vault index.
        :param mint: The mint address (optional).
        :return: Transaction signature or error details.
        """
        try:
            if vault_index < 0:
                raise ValueError("Invalid vault index.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "amount": amount,
                "vaultIndex": vault_index,
                "mint": mint if mint else None,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/squads/multisig-deposit-to-treasury",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except ValueError:
            logger.error("Invalid vault index or mint public key.", exc_info=True)
            return {"success": False, "error": "Invalid vault index or mint public key."}
        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during deposit to multisig treasury: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during deposit to multisig treasury: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def execute_multisig_proposal(
        agent: SolanaAgentKit,
        transaction_index: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Executes a multisig proposal.

        :param agent: An instance of SolanaAgentKit.
        :param transaction_index: The index of the transaction to execute.
        :return: Transaction signature or error details.
        """
        try:
            if transaction_index < 0:
                raise ValueError("Invalid transaction index.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "transactionIndex": transaction_index,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/squads/multisig-execute-proposal",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during multisig proposal execution: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during multisig proposal execution: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def reject_multisig_proposal(
        agent: SolanaAgentKit,
        transaction_index: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Rejects a multisig proposal.

        :param agent: An instance of SolanaAgentKit.
        :param transaction_index: The index of the transaction to reject.
        :return: Transaction signature or error details.
        """
        try:
            if transaction_index < 0:
                raise ValueError("Invalid transaction index.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "transactionIndex": transaction_index,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/squads/multisig-reject-proposal",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during multisig proposal rejection: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during multisig proposal rejection: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def transfer_from_multisig_treasury(
        agent: SolanaAgentKit,
        amount: float,
        to: str,
        vault_index: int,
        mint: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Transfers assets from the multisig treasury.

        :param agent: An instance of SolanaAgentKit.
        :param amount: The amount to transfer.
        :param to: The recipient address.
        :param vault_index: The index of the vault.
        :param mint: The mint address of the token to transfer.
        :return: Transaction signature or error details.
        """
        try:
            if vault_index < 0:
                raise ValueError("Invalid vault index.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "amount": amount,
                "to": to,
                "vaultIndex": vault_index,
                "mint": mint,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/squads/multisig-transfer-from-treasury",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except ValueError:
            logger.error("Invalid vault index or mint public key.", exc_info=True)
            return {"success": False, "error": "Invalid vault index or mint public key."}
        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during transfer from multisig treasury: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during transfer from multisig treasury: {error}", exc_info=True)
            return {"success": False, "error": str(error)}