import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class ThreeLandManager:
    @staticmethod
    def create_3land_collection(
        agent: SolanaAgentKit,
        collection_symbol: str,
        collection_name: str,
        collection_description: str,
        main_image_url: Optional[str] = None,
        cover_image_url: Optional[str] = None,
        is_devnet: Optional[bool] = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a 3Land NFT collection.

        :param agent: An instance of SolanaAgentKit.
        :param collection_symbol: Symbol of the collection.
        :param collection_name: Name of the collection.
        :param collection_description: Description of the collection.
        :param main_image_url: URL for the main image (optional).
        :param cover_image_url: URL for the cover image (optional).
        :param is_devnet: Boolean indicating if the operation is on devnet.
        :return: Transaction signature or error details.
        """
        try:
            if not all([collection_symbol, collection_name, collection_description]):
                raise ValueError("Collection symbol, name, and description are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "collectionSymbol": collection_symbol,
                "collectionName": collection_name,
                "collectionDescription": collection_description,
                "mainImageUrl": main_image_url,
                "coverImageUrl": cover_image_url,
                "isDevnet": is_devnet,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/nft/3land-create-collection",
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
            logger.error(f"HTTP error during 3Land collection creation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during 3Land collection creation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def create_3land_nft(
        agent: SolanaAgentKit,
        item_name: str,
        seller_fee: float,
        item_amount: int,
        item_symbol: str,
        item_description: str,
        traits: Any,
        price: Optional[float] = None,
        main_image_url: Optional[str] = None,
        cover_image_url: Optional[str] = None,
        spl_hash: Optional[str] = None,
        pool_name: Optional[str] = None,
        is_devnet: Optional[bool] = False,
        with_pool: Optional[bool] = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Mints a 3Land NFT.

        :param agent: An instance of SolanaAgentKit.
        :param item_name: Name of the NFT.
        :param seller_fee: Fee percentage for resale.
        :param item_amount: Number of NFTs to mint.
        :param item_symbol: Symbol of the NFT.
        :param item_description: Description of the NFT.
        :param traits: Metadata traits for the NFT.
        :param price: Optional price of the NFT.
        :param main_image_url: URL for the main image (optional).
        :param cover_image_url: URL for the cover image (optional).
        :param spl_hash: SPL token hash (optional).
        :param pool_name: Pool name (optional).
        :param is_devnet: Boolean indicating if the operation is on devnet.
        :param with_pool: Boolean indicating if a pool should be created.
        :return: Transaction signature or error details.
        """
        try:
            if not all([item_name, seller_fee, item_amount, item_symbol, item_description, traits]):
                raise ValueError("Item name, seller fee, amount, symbol, description, and traits are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "itemName": item_name,
                "sellerFee": seller_fee,
                "itemAmount": item_amount,
                "itemSymbol": item_symbol,
                "itemDescription": item_description,
                "traits": traits,
                "price": price,
                "mainImageUrl": main_image_url,
                "coverImageUrl": cover_image_url,
                "splHash": spl_hash,
                "poolName": pool_name,
                "isDevnet": is_devnet,
                "withPool": with_pool,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/nft/3land-create-nft",
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
            logger.error(f"HTTP error during 3Land NFT minting: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during 3Land NFT minting: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
