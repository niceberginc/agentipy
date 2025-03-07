import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent.evm import EvmAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class VirtualsManager:
    """
    Manager class to handle Virtuals functionalities such as listing, buying, and selling Sentient and Prototype tokens.
    """

    @staticmethod
    def get_sentient_listings(
        agent: EvmAgentKit,
        page_number: Optional[int] = 1,
        page_size: Optional[int] = 30,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves Sentient listings.

        :param agent: An instance of EvmAgentKit.
        :param page_number: The page number for paginated results (default: 1).
        :param page_size: The number of items per page (default: 30).
        :return: Listings data or error details.
        """
        try:
            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "rpc_api_key": agent.rpc_api_key,
                "pageNumber": page_number,
                "pageSize": page_size,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/solana/virtuals/sentient-listing",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "listings": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during fetching Sentient listings: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during fetching Sentient listings: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def buy_sentient(
        agent: EvmAgentKit,
        token_address: str,
        amount: str,
        builder_id: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Buys Sentient tokens.

        :param agent: An instance of EvmAgentKit.
        :param token_address: The token address.
        :param amount: The amount to purchase.
        :param builder_id: (Optional) The builder ID for the purchase.
        :return: Transaction receipt or error details.
        """
        try:
            if not all([token_address, amount]):
                raise ValueError("Token address and amount are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "rpc_api_key": agent.rpc_api_key,
                "tokenAddress": token_address,
                "amount": amount,
                "builderID": builder_id,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/solana/virtuals/buy-sentient",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "transaction": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during buying Sentient tokens: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during buying Sentient tokens: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def sell_sentient(
        agent: EvmAgentKit,
        token_address: str,
        amount: str,
        builder_id: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Sells Sentient tokens.

        :param agent: An instance of EvmAgentKit.
        :param token_address: The token address.
        :param amount: The amount to sell.
        :param builder_id: (Optional) The builder ID for the sale.
        :return: Transaction receipt or error details.
        """
        try:
            if not all([token_address, amount]):
                raise ValueError("Token address and amount are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "rpc_api_key": agent.rpc_api_key,
                "tokenAddress": token_address,
                "amount": amount,
                "builderID": builder_id,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/solana/virtuals/sell-sentient",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "transaction": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during selling Sentient tokens: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during selling Sentient tokens: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def buy_prototype(
        agent: EvmAgentKit,
        token_address: str,
        amount: str,
        builder_id: Optional[int] = None,
        slippage: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Buys Prototype tokens.

        :param agent: An instance of EvmAgentKit.
        :param token_address: The token address.
        :param amount: The amount to purchase.
        :param builder_id: (Optional) The builder ID for the purchase.
        :param slippage: (Optional) Slippage tolerance percentage.
        :return: Transaction receipt or error details.
        """
        try:
            if not all([token_address, amount]):
                raise ValueError("Token address and amount are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "rpc_api_key": agent.rpc_api_key,
                "tokenAddress": token_address,
                "amount": amount,
                "builderID": builder_id,
                "slippage": slippage,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/solana/virtuals/buy-prototype",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "transaction": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during buying Prototype tokens: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during buying Prototype tokens: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def sell_prototype(
        agent: EvmAgentKit,
        token_address: str,
        amount: str,
        builder_id: Optional[int] = None,
        slippage: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Sells Prototype tokens.

        :param agent: An instance of EvmAgentKit.
        :param token_address: The token address.
        :param amount: The amount to sell.
        :param builder_id: (Optional) The builder ID for the sale.
        :param slippage: (Optional) Slippage tolerance percentage.
        :return: Transaction receipt or error details.
        """
        try:
            if not all([token_address, amount]):
                raise ValueError("Token address and amount are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "rpc_api_key": agent.rpc_api_key,
                "tokenAddress": token_address,
                "amount": amount,
                "builderID": builder_id,
                "slippage": slippage,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/solana/virtuals/sell-prototype",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "transaction": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during selling Prototype tokens: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during selling Prototype tokens: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
