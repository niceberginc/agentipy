import logging
from typing import Any, Dict, List, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class LightProtocolManager:
    @staticmethod
    def send_compressed_airdrop(
        agent: SolanaAgentKit,
        mint_address: str,
        amount: float,
        decimals: int,
        recipients: List[str],
        priority_fee_in_lamports: int,
        should_log: Optional[bool] = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Sends a compressed airdrop via Light Protocol.

        :param agent: An instance of SolanaAgentKit.
        :param mint_address: Mint address of the token.
        :param amount: Amount to send.
        :param decimals: Token decimals.
        :param recipients: List of recipient wallet addresses.
        :param priority_fee_in_lamports: Priority fee in lamports.
        :param should_log: Whether to log the transaction (optional).
        :return: A dictionary containing the transaction signatures or error details.
        """
        try:
            if not all([mint_address, amount, decimals, recipients, priority_fee_in_lamports]):
                raise ValueError("Mint address, amount, decimals, recipients, and priority fee are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "mintAddress": mint_address,
                "amount": amount,
                "decimals": decimals,
                "recipients": recipients,
                "priorityFeeInLamports": priority_fee_in_lamports,
                "shouldLog": should_log,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/send-compressed-airdrop",
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
            logger.error(f"HTTP error during compressed airdrop: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during compressed airdrop: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
