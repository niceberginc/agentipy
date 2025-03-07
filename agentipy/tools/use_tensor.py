import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)


class TensorManager:
    """
    Manager class to handle Tensor functionalities such as listing NFTs for sale and canceling listings.
    """

    @staticmethod
    def list_nft_for_sale(
        agent: SolanaAgentKit,
        price: float,
        nft_mint: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Lists an NFT for sale on Tensor.

        :param agent: An instance of SolanaAgentKit.
        :param price: The listing price of the NFT.
        :param nft_mint: The mint address of the NFT.
        :return: Transaction signature or error details.
        """
        try:
            if not price or not nft_mint:
                raise ValueError("Price and NFT mint address are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "price": price,
                "nftMint": nft_mint,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/tensor/list-nft-for-sale",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during NFT listing: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during NFT listing: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def cancel_listing(
        agent: SolanaAgentKit,
        nft_mint: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Cancels a listed NFT on Tensor.

        :param agent: An instance of SolanaAgentKit.
        :param nft_mint: The mint address of the NFT to cancel the listing.
        :return: Transaction signature or error details.
        """
        try:
            if not nft_mint:
                raise ValueError("NFT mint address is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "nftMint": nft_mint,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/tensor/cancel-listing",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            return data if data.get("success") else {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during listing cancellation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during listing cancellation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
