import logging
from typing import Any, Dict, Optional
import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)


class TiplinkManager:
    """
    Manager class to handle Tiplink functionalities such as creating Tiplinks.
    """

    @staticmethod
    def create_tiplink(
        agent: SolanaAgentKit,
        amount: float,
        spl_mint_address: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a Tiplink.

        :param agent: An instance of SolanaAgentKit.
        :param amount: The amount to fund the Tiplink with.
        :param spl_mint_address: (Optional) SPL token mint address.
        :return: Transaction signature and URL or error details.
        """
        try:
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "amount": amount,
                "splMintAddress": spl_mint_address or "",  
            }

            endpoint = f"{agent.base_proxy_url}/{agent.api_version}/tiplink/create-tiplink"
            print("[DEBUG] Sending POST to:", endpoint)
            print("[DEBUG] Payload:", payload)

            response = requests.post(
                endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as http_error:
                print("[ERROR] Raw response:", response.text)
                raise http_error

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Tiplink creation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Tiplink creation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
