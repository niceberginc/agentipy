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
                f"{agent.base_proxy_url}/{agent.api_version}/base/virtuals/sentient-listing",
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
                f"{agent.base_proxy_url}/{agent.api_version}/base/virtuals/buy-sentient",
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
                f"{agent.base_proxy_url}/{agent.api_version}/base/virtuals/sell-sentient",
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
                f"{agent.base_proxy_url}/{agent.api_version}/base/virtuals/buy-prototype",
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
                f"{agent.base_proxy_url}/{agent.api_version}/base/virtuals/sell-prototype",
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

    @staticmethod
    def check_sentient_allowance(
        agent: EvmAgentKit,
        amount: str,
        from_token_address: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Checks Sentient token allowance.

        :param agent: An instance of EvmAgentKit.
        :param amount: The amount to check allowance for.
        :param from_token_address: (Optional) The address of the token being checked.
        :return: Boolean indicating whether allowance is sufficient.
        """
        try:
            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "rpc_api_key": agent.rpc_api_key,
                "amount": amount,
                "fromTokenAddress": from_token_address,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/virtuals/check-sentient-allowance",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "isAllowed": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during checking Sentient allowance: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during checking Sentient allowance: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def approve_sentient_allowance(
        agent: EvmAgentKit,
        amount: str,
        from_token_address: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Approves Sentient token allowance.

        :param agent: An instance of EvmAgentKit.
        :param amount: The amount to approve.
        :param from_token_address: (Optional) The token address being approved.
        :return: Transaction hash or error details.
        """
        try:
            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "rpc_api_key": agent.rpc_api_key,
                "amount": amount,
                "fromTokenAddress": from_token_address,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/virtuals/approve-sentient-allowance",
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
            logger.error(f"HTTP error during approving Sentient allowance: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during approving Sentient allowance: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def check_prototype_allowance(
        agent: EvmAgentKit,
        amount: str,
        from_token_address: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Checks Prototype token allowance.

        :param agent: An instance of EvmAgentKit.
        :param amount: The amount to check allowance for.
        :param from_token_address: (Optional) The address of the token being checked.
        :return: Boolean indicating whether allowance is sufficient.
        """
        try:
            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "rpc_api_key": agent.rpc_api_key,
                "amount": amount,
                "fromTokenAddress": from_token_address,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/virtuals/check-prototype-allowance",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "isAllowed": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during checking Prototype allowance: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during checking Prototype allowance: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
        
    @staticmethod
    def approve_prototype_allowance(
        agent: EvmAgentKit,
        amount: str,
        from_token_address: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Approves Prototype token allowance.

        :param agent: An instance of EvmAgentKit.
        :param amount: The amount to approve.
        :param from_token_address: (Optional) The token address being approved.
        :return: Transaction hash or error details.
        """
        try:
            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "rpc_api_key": agent.rpc_api_key,
                "amount": amount,
                "fromTokenAddress": from_token_address,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/virtuals/approve-prototype-allowance",
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
            logger.error(f"HTTP error during approving Prototype allowance: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during approving Prototype allowance: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def get_prototype_listing(
        agent: EvmAgentKit,
        page_number: int = 1,
        page_size: int = 30,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves Prototype token listings.

        :param agent: An instance of EvmAgentKit.
        :param page_number: Page number for pagination.
        :param page_size: Number of items per page.
        :return: List of Prototype token listings or error details.
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
                f"{agent.base_proxy_url}/{agent.api_version}/virtuals/get-prototype-listing",
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
            logger.error(f"HTTP error during fetching Prototype listings: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during fetching Prototype listings: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def fetch_klines(
        agent: EvmAgentKit,
        token_address: str,
        granularity: int,
        start: int,
        end: int,
        limit: int,
    ) -> Optional[Dict[str, Any]]:
        """
        Fetches Klines (candlestick chart data) for a token.

        :param agent: An instance of EvmAgentKit.
        :param token_address: The token address.
        :param granularity: The granularity of the data.
        :param start: The start timestamp.
        :param end: The end timestamp.
        :param limit: The number of data points.
        :return: Kline data or error details.
        """
        try:
            if not all([token_address, granularity, start, end, limit]):
                raise ValueError("Token address, granularity, start, end, and limit are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "rpc_api_key": agent.rpc_api_key,
                "tokenAddress": token_address,
                "granularity": granularity,
                "start": start,
                "end": end,
                "limit": limit,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/virtuals/fetch-klines",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "klines": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during fetching Klines: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during fetching Klines: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def search_virtual_token_by_keyword(
        agent: EvmAgentKit,
        keyword: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Searches for a virtual token by keyword.

        :param agent: An instance of EvmAgentKit.
        :param keyword: The search keyword.
        :return: Token details or error message.
        """
        try:
            if not keyword:
                raise ValueError("Keyword is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "rpc_api_key": agent.rpc_api_key,
                "keyword": keyword,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/virtuals/search-virtual-token-by-keyword",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "token": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during searching virtual token: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during searching virtual token: {error}", exc_info=True)
            return {"success": False, "error": str(error)}