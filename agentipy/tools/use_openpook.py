import logging
from typing import Any, Dict, List, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class OpenBookManager:
    @staticmethod
    def create_market(
        agent: SolanaAgentKit,
        base_mint: str,
        quote_mint: str,
        lot_size: Optional[float] = 1,
        tick_size: Optional[float] = 0.01,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a market on OpenBook.

        :param agent: An instance of SolanaAgentKit.
        :param base_mint: The base asset mint address.
        :param quote_mint: The quote asset mint address.
        :param lot_size: Lot size (default: 1).
        :param tick_size: Tick size (default: 0.01).
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
                "lotSize": lot_size,
                "tickSize": tick_size,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/openbook-create-market",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transactions": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during OpenBook market creation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during OpenBook market creation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
