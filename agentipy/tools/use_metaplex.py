import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class DeployCollectionManager:
    @staticmethod
    def deploy_collection(
        agent: SolanaAgentKit,
        name: str,
        uri: str,
        royalty_basis_points: int,
        creator_address: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Deploys an NFT collection via an HTTP request to the agent toolkit API.

        :param agent: An instance of SolanaAgentKit configured with required credentials.
        :param name: The name of the NFT collection.
        :param uri: The metadata URI for the collection.
        :param royalty_basis_points: The royalty percentage in basis points (e.g., 500 for 5%).
        :param creator_address: The public key of the collection's creator.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not all([name, uri, royalty_basis_points, creator_address]):
                raise ValueError("Name, URI, royalty_basis_points, and creator_address are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "name": name,
                "uri": uri,
                "royaltyBasisPoints": royalty_basis_points,
                "creatorAddress": creator_address,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/nft/deploy-collection",
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
            logger.error(f"HTTP error during collection deployment: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during collection deployment: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
        
    @staticmethod
    def get_metaplex_asset(
        agent: SolanaAgentKit,
        assetId: str
    ) -> Optional[Dict[str, Any]]:
        """
        Fetches detailed information about a specific asset using an HTTP request to the agent toolkit API.

        :param agent: An instance of SolanaAgentKit configured with the required credentials and RPC settings.
        :param assetId: The unique identifier of the asset to be fetched.
        :return: A dictionary containing the asset details or error information.
        """
        try:
            if not all([assetId]):
                raise ValueError("assetId is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "assetId": assetId,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/nft/get-asset",
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
            logger.error(f"HTTP error during collection deployment: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during collection deployment: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
        
    @staticmethod
    def get_metaplex_assets_by_creator(
        agent: SolanaAgentKit,
        creator: str,
        onlyVerified: bool = False,
        sortBy: Optional[str] = None,
        sortDirection: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Fetches assets created by a specific creator using an HTTP request to the agent toolkit API.

        :param agent: An instance of SolanaAgentKit configured with the required credentials and RPC settings.
        :param creator: The public key of the creator whose assets are to be fetched.
        :param onlyVerified: (Optional) A flag indicating whether to fetch only verified assets (default is False).
        :param sortBy: (Optional) The field by which to sort the assets (e.g., "date", "name").
        :param sortDirection: (Optional) The direction of sorting, either "asc" for ascending or "desc" for descending.
        :param limit: (Optional) The maximum number of assets to retrieve.
        :param page: (Optional) The page number for paginated results.
        :param before: (Optional) Fetch assets listed before this cursor.
        :param after: (Optional) Fetch assets listed after this cursor.
        :return: A dictionary containing the fetched assets or error details.
        """
        try:
            if not all([creator]):
                raise ValueError("creator is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "creator": creator,
                "onlyVerified": onlyVerified,
                "sortBy": sortBy,
                "sortDirection": sortDirection,
                "limit": limit,
                "page": page,
                "before": before,
                "after": after,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/nft/get-assets-by-creator",
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
            logger.error(f"HTTP error during collection deployment: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during collection deployment: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
        
    @staticmethod
    def get_metaplex_assets_by_authority(
        agent: SolanaAgentKit,
        authority: str,
        sortBy: Optional[str] = None,
        sortDirection: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Fetches assets associated with a specific authority using an HTTP request to the agent toolkit API.

        :param agent: An instance of SolanaAgentKit configured with the required credentials and RPC settings.
        :param authority: The public key of the authority whose assets are to be fetched.
        :param sortBy: (Optional) The field by which to sort the assets (e.g., "date", "name").
        :param sortDirection: (Optional) The direction of sorting, either "asc" for ascending or "desc" for descending.
        :param limit: (Optional) The maximum number of assets to retrieve.
        :param page: (Optional) The page number for paginated results.
        :param before: (Optional) Fetch assets listed before this cursor.
        :param after: (Optional) Fetch assets listed after this cursor.
        :return: A dictionary containing the fetched assets or error details.
        """
        try:
            if not all([authority]):
                raise ValueError("authority is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "authority": authority,
                "sortBy": sortBy,
                "sortDirection": sortDirection,
                "limit": limit,
                "page": page,
                "before": before,
                "after": after,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/nft/get-assets-by-authority",
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
            logger.error(f"HTTP error during collection deployment: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during collection deployment: {error}", exc_info=True)
            return {"success": False, "error": str(error)}
        
    @staticmethod
    def mint_metaplex_core_nft(
        agent: SolanaAgentKit,
        collectionMint: str,
        name: str,
        uri: str,
        sellerFeeBasisPoints: Optional[int] = None,
        address: Optional[str] = None,
        share: Optional[str] = None,
        recipient: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Mints an NFT using the Metaplex Core program via an HTTP request to the agent toolkit API.

        :param agent: An instance of SolanaAgentKit configured with the required credentials and RPC settings.
        :param collectionMint: The public key of the collection mint to which the NFT belongs.
        :param name: The name of the NFT to be minted.
        :param uri: The metadata URI containing information about the NFT (e.g., image, description).
        :param sellerFeeBasisPoints: (Optional) The royalty percentage in basis points (e.g., 500 for 5% royalties).
        :param address: (Optional) The public key of the creator's address for the NFT.
        :param share: (Optional) The share percentage for the creator (e.g., 100 for 100%).
        :param recipient: (Optional) The public key of the wallet to receive the minted NFT. Defaults to the agent's wallet if not provided.
        :return: A dictionary containing the transaction signature, success status, and any error details.
        """
        try:
            if not all([collectionMint, name, uri]):
                raise ValueError("collectionMint, name, uri is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "collectionMint": collectionMint,
                "name": name,
                "uri": uri,
                "sellerFeeBasisPoints": sellerFeeBasisPoints,
                "address": address,
                "share": share,
                "recipient": recipient,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/nft/mint",
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
            logger.error(f"HTTP error during collection deployment: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during collection deployment: {error}", exc_info=True)
            return {"success": False, "error": str(error)}