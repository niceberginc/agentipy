import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class AdrenaTradeManager:
    @staticmethod
    def close_perp_trade_short(
        agent: SolanaAgentKit,
        price: float,
        trade_mint: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Closes a perpetual short trade.

        :param agent: An instance of SolanaAgentKit.
        :param price: Trade closing price.
        :param trade_mint: The mint address of the trade asset.
        :return: Transaction signature or error details.
        """
        try:
            if not all([price, trade_mint]):
                raise ValueError("Price and trade_mint are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "price": price,
                "tradeMint": trade_mint,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/adrena/close-perp-trade-short",
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
            logger.error(f"HTTP error during close perp trade short: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during close perp trade short: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def close_perp_trade_long(
        agent: SolanaAgentKit,
        price: float,
        trade_mint: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Closes a perpetual long trade.

        :param agent: An instance of SolanaAgentKit.
        :param price: Trade closing price.
        :param trade_mint: The mint address of the trade asset.
        :return: Transaction signature or error details.
        """
        try:
            if not all([price, trade_mint]):
                raise ValueError("Price and trade_mint are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "price": price,
                "tradeMint": trade_mint,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/adrena/close-perp-trade-long",
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
            logger.error(f"HTTP error during close perp trade long: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during close perp trade long: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
    
    @staticmethod
    def open_perp_trade_long(
        agent: SolanaAgentKit,
        price: float,
        collateral_amount: float,
        collateral_mint: Optional[str] = None,
        leverage: Optional[float] = None,
        trade_mint: Optional[str] = None,
        slippage: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Opens a perpetual long trade.
        """
        try:
            if not all([price, collateral_amount]):
                raise ValueError("Price and collateral_amount are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "price": price,
                "collateralAmount": collateral_amount,
                "collateralMint": collateral_mint,
                "leverage": leverage,
                "tradeMint": trade_mint,
                "slippage": slippage,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/adrena/open-perp-trade-long",
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
            logger.error(f"HTTP error during open perp trade long: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during open perp trade long: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def open_perp_trade_short(
        agent: SolanaAgentKit,
        price: float,
        collateral_amount: float,
        collateral_mint: Optional[str] = None,
        leverage: Optional[float] = None,
        trade_mint: Optional[str] = None,
        slippage: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Opens a perpetual short trade.
        """
        try:
            if not all([price, collateral_amount]):
                raise ValueError("Price and collateral_amount are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "price": price,
                "collateralAmount": collateral_amount,
                "collateralMint": collateral_mint,
                "leverage": leverage,
                "tradeMint": trade_mint,
                "slippage": slippage,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/adrena/open-perp-trade-short",
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
            logger.error(f"HTTP error during open perp trade short: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during open perp trade short: {error}", exc_info=True)
            return {"success": False, "error": str(error)}