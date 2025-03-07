import logging
from typing import Any, Dict, List, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class SolutiofiManager:
    """
    Manager class to handle Solutiofi functionalities such as closing accounts,
    burning tokens, merging tokens, and spreading tokens.
    """

    @staticmethod
    def close_accounts(
        agent: SolanaAgentKit,
        mints: List[str],
    ) -> Optional[Dict[str, Any]]:
        """
        Closes token accounts.

        :param agent: An instance of SolanaAgentKit.
        :param mints: List of mint addresses to close.
        :return: List of transaction signatures or error details.
        """
        try:
            if not mints:
                raise ValueError("Mints list cannot be empty.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "solutiofi_api_key": agent.solutiofi_api_key,
                "mints": mints,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/solutiofi/close-accounts",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "transactions": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during closing accounts: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during closing accounts: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def burn_tokens(
        agent: SolanaAgentKit,
        mints: List[str],
    ) -> Optional[Dict[str, Any]]:
        """
        Burns tokens from specific mint addresses.

        :param agent: An instance of SolanaAgentKit.
        :param mints: List of mint addresses to burn tokens from.
        :return: List of transaction signatures or error details.
        """
        try:
            if not mints:
                raise ValueError("Mints list cannot be empty.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "solutiofi_api_key": agent.solutiofi_api_key,
                "mints": mints,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/solutiofi/burn-tokens",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "transactions": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during burning tokens: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during burning tokens: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def merge_tokens(
        agent: SolanaAgentKit,
        input_assets: List[Dict[str, Any]],
        output_mint: str,
        priority_fee: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Merges tokens into a single output mint.

        :param agent: An instance of SolanaAgentKit.
        :param input_assets: List of input assets.
        :param output_mint: The mint address of the output token.
        :param priority_fee: Priority fee level ('fast', 'turbo', 'ultra').
        :return: List of transaction signatures or error details.
        """
        try:
            if not input_assets or not output_mint or not priority_fee:
                raise ValueError("Input assets, output mint, and priority fee are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "solutiofi_api_key": agent.solutiofi_api_key,
                "inputAssets": input_assets,
                "outputMint": output_mint,
                "priorityFee": priority_fee,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/solutiofi/merge-tokens",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "transactions": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during merging tokens: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during merging tokens: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def spread_token(
        agent: SolanaAgentKit,
        input_asset: Dict[str, Any],
        target_tokens: List[Dict[str, Any]],
        priority_fee: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Spreads an input token into multiple target tokens.

        :param agent: An instance of SolanaAgentKit.
        :param input_asset: The asset to be spread.
        :param target_tokens: List of target token distributions.
        :param priority_fee: Priority fee level ('fast', 'turbo', 'ultra').
        :return: List of transaction signatures or error details.
        """
        try:
            if not input_asset or not target_tokens or not priority_fee:
                raise ValueError("Input asset, target tokens, and priority fee are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "solutiofi_api_key": agent.solutiofi_api_key,
                "inputAsset": input_asset,
                "targetTokens": target_tokens,
                "priorityFee": priority_fee,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/solutiofi/spread-token",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "transactions": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during spreading tokens: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during spreading tokens: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
