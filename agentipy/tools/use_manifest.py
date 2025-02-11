import logging
from typing import Any, Dict, List, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class ManifestManager:
    @staticmethod
    def create_market(
        agent: SolanaAgentKit,
        base_mint: str,
        quote_mint: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a market using the Manifest protocol.

        :param agent: An instance of SolanaAgentKit.
        :param base_mint: The base asset mint address.
        :param quote_mint: The quote asset mint address.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not all([base_mint, quote_mint]):
                raise ValueError("Base mint and quote mint are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "baseMint": base_mint,
                "quoteMint": quote_mint,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/manifest-create-market",
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
            logger.error(f"HTTP error during market creation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during market creation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def place_limit_order(
        agent: SolanaAgentKit,
        market_id: str,
        quantity: float,
        side: str,
        price: float,
    ) -> Optional[Dict[str, Any]]:
        """
        Places a limit order on the Manifest protocol.

        :param agent: An instance of SolanaAgentKit.
        :param market_id: The market ID.
        :param quantity: The amount to trade.
        :param side: The order side, either "buy" or "sell".
        :param price: The limit price.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not all([market_id, quantity, side, price]):
                raise ValueError("Market ID, quantity, side, and price are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "marketId": market_id,
                "quantity": quantity,
                "side": side,
                "price": price,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/limit-order",
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
            logger.error(f"HTTP error during limit order placement: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during limit order placement: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def place_batch_orders(
        agent: SolanaAgentKit,
        market_id: str,
        orders: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """
        Places multiple limit orders on the Manifest protocol.

        :param agent: An instance of SolanaAgentKit.
        :param market_id: The market ID.
        :param orders: A list of orders, each containing quantity, side, and price.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not market_id or not orders:
                raise ValueError("Market ID and orders are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "marketId": market_id,
                "orders": orders,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/batch-order",
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
            logger.error(f"HTTP error during batch order placement: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during batch order placement: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def cancel_all_orders(
        agent: SolanaAgentKit,
        market_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Cancels all orders on a given market.

        :param agent: An instance of SolanaAgentKit.
        :param market_id: The market ID.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not market_id:
                raise ValueError("Market ID is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "marketId": market_id,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/cancel-all-orders",
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
            logger.error(f"HTTP error during order cancellation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during order cancellation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
        
    @staticmethod
    def withdraw_all(
        agent: SolanaAgentKit,
        market_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Withdraws all assets from a given market.

        :param agent: An instance of SolanaAgentKit.
        :param market_id: The market ID.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not market_id:
                raise ValueError("Market ID is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "marketId": market_id,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/withdraw-all",
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
            logger.error(f"HTTP error during withdrawal: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during withdrawal: {error}", exc_info=True)
            return {"success": False, "error": str(error)}