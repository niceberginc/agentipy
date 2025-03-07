import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)


class SwitchboardManager:
    """
    Manager class to handle Switchboard functionalities such as simulating a Switchboard feed.
    """

    @staticmethod
    def simulate_switchboard_feed(
        agent: SolanaAgentKit,
        feed: str,
        crossbar_url: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Simulates a Switchboard feed.

        :param agent: An instance of SolanaAgentKit.
        :param feed: The feed to be simulated.
        :param crossbar_url: The crossbar URL for Switchboard (default provided).
        :return: The result of the simulation or error details.
        """
        try:
            if not feed:
                raise ValueError("Feed is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "feed": feed,
                "crossbarUrl": crossbar_url if crossbar_url else None
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/switchboard/simulate-switchboard-feed",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Switchboard feed simulation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Switchboard feed simulation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
