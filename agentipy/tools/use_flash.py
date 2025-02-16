import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class FlashTradeManager:
    @staticmethod
    def flash_open_trade(
        agent: SolanaAgentKit,
        token: str,
        side: str,
        collateral_usd: float,
        leverage: float,
    ) -> Optional[Dict[str, Any]]:
        """
        Opens a flash trade using the agent toolkit API.

        :param agent: An instance of SolanaAgentKit configured with required credentials.
        :param token: The trading token.
        :param side: The trade direction ("buy" or "sell").
        :param collateral_usd: The collateral amount in USD.
        :param leverage: The leverage multiplier.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not all([token, side, collateral_usd, leverage]):
                raise ValueError("Token, side, collateral_usd, and leverage are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "token": token,
                "side": side,
                "collateralUsd": collateral_usd,
                "leverage": leverage,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/flash/flash-open-trade",
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
            logger.error(f"HTTP error during flash trade open: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during flash trade open: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def flash_close_trade(
        agent: SolanaAgentKit,
        token: str,
        side: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Closes a flash trade using the agent toolkit API.

        :param agent: An instance of SolanaAgentKit configured with required credentials.
        :param token: The trading token.
        :param side: The trade direction ("buy" or "sell").
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not all([token, side]):
                raise ValueError("Token and side are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "token": token,
                "side": side,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/flash/flash-close-trade",
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
            logger.error(f"HTTP error during flash trade close: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during flash trade close: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
