import base64
import json
from typing import Dict, Optional, Any, List
import requests

from solders.pubkey import Pubkey  # type: ignore
from solders.instruction import Instruction
from solders.keypair import Keypair
from solana.rpc.api import Client as SolanaClient
from .base_wallet_client import BaseWalletClient
from .solana_wallet_client import SolanaTransaction


class PrivyWalletClient(BaseWalletClient):
    """Privy wallet implementation for Solana."""

    BASE_URL = "https://api.privy.io"

    def __init__(self, client: SolanaClient, app_id: str, app_secret: str):
        """
        Initialize the Privy wallet client.

        Args:
            app_id: Privy application ID
            app_secret: Privy application secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.client = client
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

    def use_wallet(self, wallet_id: str) -> Dict[str, str]:

        payload = {"chain_type": "solana"}
        url = f"{self.BASE_URL}/v1/wallets/{wallet_id}"

        response = requests.get(url, headers=self._get_auth_headers(), json=payload)
        response_data = response.json()
        print(response_data)

        if response.status_code != 200:
            raise Exception(f"Failed to use wallet: {response_data}")

        self.wallet_address = response_data["address"]
        self.wallet_id = wallet_id

        return self.wallet_address

    def get_all_wallets(self) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/v1/wallets"

        response = requests.get(url, headers=self._get_auth_headers())
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f"Failed to get wallets: {response_data}")

        return response_data

    def create_wallet(self) -> Dict[str, str]:
        """Create a new Solana wallet using Privy API."""
        url = f"{self.BASE_URL}/v1/wallets"

        payload = {"chain_type": "solana"}

        response = requests.post(url, headers=self._get_auth_headers(), json=payload)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f"Failed to create wallet: {response_data}")

        self.wallet_id = response_data["id"]
        self.wallet_address = response_data["address"]

        print("wallet_id", self.wallet_id)

        return {"id": self.wallet_id, "address": self.wallet_address}

    def get_address(self) -> str:
        """Get the wallet address."""
        if not self.wallet_address:
            raise ValueError("Wallet not initialized. Call create_wallet first.")
        return self.wallet_address

    def sign_message(self, message: str) -> Dict[str, str]:
        """Sign a message with the wallet."""
        if not self.wallet_id:
            raise ValueError("Wallet not initialized. Call create_wallet first.")

        url = f"{self.BASE_URL}/v1/wallets/{self.wallet_id}/rpc"

        payload = {
            "method": "signMessage",
            "caip2": "solana:1",  # Solana mainnet
            "chain_type": "solana",
            "params": {"message": message},
        }

        response = requests.post(url, headers=self._get_auth_headers(), json=payload)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f"Failed to sign message: {response_data}")

        return {"signature": response_data["data"]["signature"]}

    def balance_of(self, address: str) -> Dict:
        pubkey = Pubkey.from_string(address)
        balance_lamports = self.client.get_balance(pubkey).value
        return {
            "decimals": 9,
            "symbol": "SOL",
            "value": str(balance_lamports / 10**9),
            "in_base_units": str(balance_lamports),
        }

    def send_transaction(self, transactionData) -> Dict[str, str]:
        """Send a Solana transaction using Privy API."""
        if not self.wallet_id:
            raise ValueError("Wallet not initialized. Call create_wallet first.")

        BASE_URL = "https://auth.privy.io"
        url = f"{BASE_URL}/v1/wallets/{self.wallet_id}/rpc"

        payload = {
            "method": "signAndSendTransaction",
            "caip2": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",  # Solana mainnet
            "params": {
                "transaction": transactionData,
                "encoding": "base64",
            },
        }

        try:
            print("Sending transaction to Privy API...")

            response = requests.post(
                url, headers=self._get_auth_headers(), json=payload
            )

            print(f"Response status: {response.status_code}")

            try:
                response_data = response.json()
                print(f"Response data: {json.dumps(response_data)}")

                if response.status_code != 200:
                    raise Exception(
                        f"Failed to send transaction: {json.dumps(response_data)}"
                    )

                return {"hash": response_data["data"]["hash"]}

            except json.JSONDecodeError:
                print("Response is not valid JSON")
                if response.status_code != 200:
                    raise Exception(f"Failed to send transaction: {response.text}")

        except requests.exceptions.RequestException as error:
            print(f"Error response: {error}")
            if hasattr(error, "response") and error.response:
                try:
                    error_data = error.response.json()
                    print(f"Error response: {json.dumps(error_data)}")
                    raise Exception(
                        f"Failed to send transaction: {json.dumps(error_data)}"
                    )
                except json.JSONDecodeError:
                    raise Exception(
                        f"Failed to send transaction: {error.response.text}"
                    )
            raise error
