import logging
from typing import Any, Dict, List, Optional

import requests
from solders.pubkey import Pubkey as PublicKey  # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class AllDomainsManager:
    @staticmethod
    def resolve_all_domains(agent: SolanaAgentKit, domain: str) -> Optional[str]:
        """
        Resolves all domain types associated with a given domain name.

        Args:
            agent (SolanaAgentKit): The agent instance.
            domain (str): The domain name.

        Returns:
            Optional[str]: The resolved domain's TLD.
        """
        try:
            if not domain:
                raise ValueError("Domain is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "domain": domain,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/domains/resolve-all-domains",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return data.get("value")
            else:
                return None
        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error resolving domain: {http_error}", exc_info=True)
            return None
        except Exception as error:
            logger.error(f"Unexpected error resolving domain: {error}", exc_info=True)
            return None

    @staticmethod
    def get_owned_domains_for_tld(agent: SolanaAgentKit, tld: str) -> Optional[List[str]]:
        """
        Retrieves the domains owned by the user for a given TLD.

        Args:
            agent (SolanaAgentKit): The agent instance.
            tld (str): The top-level domain (TLD).

        Returns:
            Optional[List[str]]: List of owned domains.
        """
        try:
            if not tld:
                raise ValueError("TLD is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "tld": tld,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/domains/get-owned-domains-for-tld",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            return data.get("value", [])
        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error fetching owned domains: {http_error}", exc_info=True)
            return None
        except Exception as error:
            logger.error(f"Unexpected error fetching owned domains: {error}", exc_info=True)
            return None

    @staticmethod
    def get_all_domains_tlds(agent: SolanaAgentKit) -> Optional[List[str]]:
        """
        Retrieves all available TLDs.

        Args:
            agent (SolanaAgentKit): The agent instance.

        Returns:
            Optional[List[str]]: List of available TLDs.
        """
        try:
            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/domains/get-all-domains-tlds",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            return data.get("value", [])
        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error fetching all domains TLDs: {http_error}", exc_info=True)
            return None
        except Exception as error:
            logger.error(f"Unexpected error fetching all domains TLDs: {error}", exc_info=True)
            return None

    @staticmethod
    def get_owned_all_domains(agent: SolanaAgentKit, owner: str) -> Optional[List[str]]:
        """
        Retrieves all domains owned by a given user.

        Args:
            agent (SolanaAgentKit): The agent instance.
            owner (str): The owner's public key.

        Returns:
            Optional[List[str]]: List of owned domains.
        """
        try:
            if not owner:
                raise ValueError("Owner is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            owner_pubkey = PublicKey(owner)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "owner": str(owner_pubkey),
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/domains/get-owned-all-domains",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            return data.get("value", [])
        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error fetching owned all domains: {http_error}", exc_info=True)
            return None
        except Exception as error:
            logger.error(f"Unexpected error fetching owned all domains: {error}", exc_info=True)
            return None
