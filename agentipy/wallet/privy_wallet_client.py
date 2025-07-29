import base64
import json
from typing import Any, Dict, List, Optional, Union

import requests
from eth_utils.address import to_checksum_address
from solana.rpc.api import Client as SolanaClient
from solders.instruction import Instruction  # type: ignore
from solders.keypair import Keypair  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from web3 import Web3
from web3.types import Wei

from .base_wallet_client import BaseWalletClient
from .evm_wallet_client import EVMTransaction, WalletClientInterface
from .solana_wallet_client import SolanaTransaction


class ChainType:
    """Supported chain types in Privy"""

    SOLANA = "solana"
    EVM = "evm"


class PrivyWalletClient(BaseWalletClient, WalletClientInterface):
    """Privy wallet implementation for Solana and EVM chains."""

    BASE_URL = "https://api.privy.io"
    AUTH_URL = "https://auth.privy.io"

    def __init__(
        self,
        client: Union[SolanaClient, Web3],
        app_id: str,
        app_secret: str,
        chain_type: str = ChainType.SOLANA,
        chain_id: Optional[int] = None,
    ):
        """
        Initialize the Privy wallet client.

        Args:
            client: SolanaClient for Solana or Web3 for EVM
            app_id: Privy application ID
            app_secret: Privy application secret
            chain_type: Type of blockchain (solana or evm)
            chain_id: Chain ID for EVM chains
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.client = client
        self.chain_type = chain_type
        self.chain_id = chain_id
        self.wallet_id = None
        self.wallet_address = None

    def _get_auth_headers(self):
        """Get the authentication headers for Privy API requests."""
        auth_string = f"{self.app_id}:{self.app_secret}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()

        return {
            "Authorization": f"Basic {encoded_auth}",
            "privy-app-id": self.app_id,
            "Content-Type": "application/json",
        }

    def _get_caip2(self):
        """Get the CAIP-2 chain identifier based on chain type and ID."""
        if self.chain_type == ChainType.SOLANA:
            return (
                "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d"  # Solana mainnet
            )
        elif self.chain_type == ChainType.EVM:
            return f"eip155:{self.chain_id}"  # EVM with chain ID
        else:
            raise ValueError(f"Unsupported chain type: {self.chain_type}")

    def use_wallet(self, wallet_id: str) -> str:
        """Use an existing wallet from Privy."""
        payload = {"chain_type": self.chain_type}
        url = f"{self.BASE_URL}/v1/wallets/{wallet_id}"

        response = requests.get(url, headers=self._get_auth_headers(), json=payload)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f"Failed to use wallet: {response_data}")

        self.wallet_address = response_data["address"]
        self.wallet_id = wallet_id

        return self.wallet_address

    def get_all_wallets(self) -> List[Dict[str, Any]]:
        """Get all wallets associated with the Privy app."""
        url = f"{self.BASE_URL}/v1/wallets"

        response = requests.get(url, headers=self._get_auth_headers())
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f"Failed to get wallets: {response_data}")

        return response_data

    def create_wallet(self) -> Dict[str, str]:
        """Create a new wallet using Privy API."""
        url = f"{self.BASE_URL}/v1/wallets"

        if self.chain_type == ChainType.SOLANA:
            payload = {"chain_type": self.chain_type}
        elif self.chain_type == ChainType.EVM:
            payload = {"chain_type": "ethereum", "chain_id": self.chain_id}

        response = requests.post(url, headers=self._get_auth_headers(), json=payload)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f"Failed to create wallet: {response_data}")

        self.wallet_id = response_data["id"]
        self.wallet_address = response_data["address"]

        return {"id": self.wallet_id, "address": self.wallet_address}

    def get_address(self) -> str:
        """Get the wallet address."""
        if not self.wallet_address:
            raise ValueError(
                "Wallet not initialized. Call create_wallet or use_wallet first."
            )
        return self.wallet_address

    def sign_message(self, message: str) -> Dict[str, str]:
        """Sign a message with the wallet."""
        if not self.wallet_id:
            raise ValueError(
                "Wallet not initialized. Call create_wallet or use_wallet first."
            )

        url = f"{self.BASE_URL}/v1/wallets/{self.wallet_id}/rpc"

        payload = {
            "method": "signMessage",
            "caip2": self._get_caip2(),
            "chain_type": self.chain_type,
            "params": {"message": message},
        }

        response = requests.post(url, headers=self._get_auth_headers(), json=payload)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f"Failed to sign message: {response_data}")

        return {"signature": response_data["data"]["signature"]}

    def balance_of(self, address: Optional[str] = None) -> Dict:
        """Get the balance of the specified address."""
        if not address:
            address = self.wallet_address

        if not address:
            raise ValueError("No address provided and wallet not initialized.")

        if self.chain_type == ChainType.SOLANA:
            # Solana balance query
            pubkey = Pubkey.from_string(address)
            balance_lamports = self.client.get_balance(pubkey).value
            return {
                "decimals": 9,
                "symbol": "SOL",
                "value": str(balance_lamports / 10**9),
                "in_base_units": str(balance_lamports),
            }
        elif self.chain_type == ChainType.EVM:
            # EVM balance query
            balance_wei = self.client.eth.get_balance(to_checksum_address(address))
            return {
                "decimals": 18,
                "symbol": "ETH",  # This would ideally be dynamic based on the chain
                "value": str(Web3.from_wei(balance_wei, "ether")),
                "in_base_units": str(balance_wei),
            }
        else:
            raise ValueError(f"Unsupported chain type: {self.chain_type}")

    async def send_transaction(self, transaction_data: Any) -> Dict[str, str]:
        """
        Send a transaction using Privy API.

        For Solana: transaction_data should be base64 encoded transaction
        For EVM: transaction_data should be an EVMTransaction object
        """
        if not self.wallet_id:
            raise ValueError(
                "Wallet not initialized. Call create_wallet or use_wallet first."
            )

        # Default URL (used for EVM eth_sendTransaction)
        url = f"{self.BASE_URL}/v1/wallets/{self.wallet_id}/rpc"

        if self.chain_type == ChainType.SOLANA:
            # Use AUTH_URL for signAndSendTransaction for Solana
            url = f"{self.AUTH_URL}/v1/wallets/{self.wallet_id}/rpc"
            payload = {
                "method": "signAndSendTransaction",
                # Hardcoded Solana Mainnet CAIP-2
                "caip2": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
                "params": {
                    "transaction": transaction_data,  # Expects base64 encoded string
                    "encoding": "base64",
                },
            }
        elif self.chain_type == ChainType.EVM:
            if not isinstance(transaction_data, EVMTransaction):
                raise TypeError(
                    "transaction_data must be an EVMTransaction for EVM chains"
                )

            # Construct the transaction object for eth_sendTransaction
            evm_transaction_param = {
                "to": transaction_data.to,
                "value": hex(
                    transaction_data.value
                ),  # Value must be hex encoded string
            }
            # Include data if present (for contract interactions)
            if transaction_data.data and transaction_data.data != "0x":
                evm_transaction_param["data"] = transaction_data.data
            # Include gas if provided
            if transaction_data.gas:
                evm_transaction_param["gas"] = hex(transaction_data.gas)

            payload = {
                "method": "eth_sendTransaction",
                # Hardcoded EVM CAIP-2 (Base Mainnet)
                "caip2": "eip155:8453",
                "params": {
                    "transaction": evm_transaction_param,
                },
            }
        else:
            raise ValueError(f"Unsupported chain type: {self.chain_type}")

        # Use appropriate headers (auth headers are needed for both endpoints)
        headers = self._get_auth_headers()
        # Privy docs for eth_sendTransaction show using -u for basic auth AND privy-app-id header.
        # The _get_auth_headers already includes both Authorization: Basic and privy-app-id.

        try:
            response = requests.post(url, headers=headers, json=payload)

            try:
                response_data = response.json()

                if response.status_code != 200:
                    raise Exception(
                        f"Failed to send transaction: {json.dumps(response_data)}"
                    )

                return {"hash": response_data["data"]["hash"]}

            except json.JSONDecodeError:
                if response.status_code != 200:
                    raise Exception(f"Failed to send transaction: {response.text}")

        except requests.exceptions.RequestException as error:
            if hasattr(error, "response") and error.response:
                try:
                    error_data = error.response.json()
                    raise Exception(
                        f"Failed to send transaction: {json.dumps(error_data)}"
                    )
                except json.JSONDecodeError:
                    raise Exception(
                        f"Failed to send transaction: {error.response.text}"
                    )
            raise error
