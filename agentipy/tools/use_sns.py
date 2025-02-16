import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent import SolanaAgentKit

logger = logging.getLogger(__name__)

class NameServiceManager:
    @staticmethod
    def resolve_name_to_address(agent: SolanaAgentKit, domain: str) -> Optional[str]:
        """
        Resolves a Solana Name Service domain to its corresponding address using QuickNode RPC.

        :param domain: The SNS domain (e.g., example.sol).
        :return: The associated Solana address or None if not found.
        """
        try:
            if not domain:
                raise ValueError("Domain name is required")

            payload = {
                "id": 42,
                "jsonrpc": "2.0",
                "method": "sns_resolveDomain",
                "params": [domain]
            }

            response = requests.post(
                agent.quicknode_rpc_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            return data.get("result")
        except Exception as error:
            logger.error(f"Error resolving domain to address: {str(error)}", exc_info=True)
            return None
        
    @staticmethod
    def get_favourite_domain(agent: SolanaAgentKit, owner: str) -> Optional[str]:
        """
        Resolves a Solana Name Service domain to its corresponding address using QuickNode RPC.

        :param domain: The SNS domain (e.g., example.sol).
        :return: The associated Solana address or None if not found.
        """
        try:
            if not owner:
                raise ValueError("Domain name is required")

            payload = {
                "id": 42,
                "jsonrpc": "2.0",
                "method": "sns_getFavouriteDomain",
                "params": [owner]
            }

            response = requests.post(
                agent.quicknode_rpc_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            return data.get("result")
        except Exception as error:
            logger.error(f"Error resolving domain to address: {str(error)}", exc_info=True)
            return None
        
    @staticmethod
    def get_all_domains_for_owner(agent: SolanaAgentKit, owner: str) -> Optional[str]:
        """
        Resolves a Solana Name Service domain to its corresponding address using QuickNode RPC.

        :param domain: The SNS domain (e.g., example.sol).
        :return: The associated Solana address or None if not found.
        """
        try:
            if not owner:
                raise ValueError("Domain name is required")

            payload = {
                "id": 42,
                "jsonrpc": "2.0",
                "method": "sns_getAllDomainsForOwner",
                "params": [owner]
            }

            response = requests.post(
                agent.quicknode_rpc_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            return data.get("result")
        except Exception as error:
            logger.error(f"Error resolving domain to address: {str(error)}", exc_info=True)
            return None
        
    @staticmethod
    def get_registration_transaction(agent:SolanaAgentKit, domain: str, buyer: str, buyer_token_account: str, space: int, 
                                     mint: Optional[str] = None, referrer_key: Optional[str] = None) -> Optional[str]:
        """
        Returns a ready-to-sign, base64-encoded transaction object to register a new SNS domain.

        :param domain: The domain name to register.
        :param buyer: The base58-encoded Solana public key of the buyer's paying wallet.
        :param buyer_token_account: The base58-encoded Solana public key of the buyer's paying token account.
        :param space: The number of bytes to allocate in the new registered domain.
        :param mint: (Optional) The Solana public key of the Token mint used for payment, defaults to USDC.
        :param referrer_key: (Optional) The base58-encoded Solana public key of the registration referrer.
        :return: The base64-encoded Solana transaction object or None if an error occurs.
        """
        try:
            if not all([domain, buyer, buyer_token_account, space]):
                raise ValueError("Domain, buyer, buyer_token_account, and space are required")

            payload: Dict[str, Any] = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "sns_getRegistrationTransaction",
                "params": [
                    domain,
                    buyer,
                    buyer_token_account,
                    space
                ]
            }

            if mint:
                payload["params"].append(mint)
            if referrer_key:
                payload["params"].append(referrer_key)

            response = requests.post(
                agent.quicknode_rpc_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            return data.get("result")
        except Exception as error:
            logger.error(f"Error getting registration transaction: {str(error)}", exc_info=True)
            return None