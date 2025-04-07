from typing import Dict, Optional, Union
import logging
import requests
from web3 import Web3
from agentipy.utils import AgentKitError
from agentipy.wallet.evm_wallet_client import EVMTransaction, WalletClientInterface

logger = logging.getLogger(__name__)


class CrossmintWallet:
    """Represents a Crossmint wallet configuration."""

    def __init__(self, wallet_data: Dict):
        self.type = wallet_data.get("type")
        self.address = wallet_data.get("address")
        self.config = wallet_data.get("config", {})

    @property
    def id(self) -> str:
        """Return the wallet address as ID."""
        return self.address

    @classmethod
    def from_dict(cls, data: Dict) -> "CrossmintWallet":
        """Create a CrossmintWallet instance from a dictionary."""
        # Filter out createdAt data
        if "createdAt" in data:
            data = {k: v for k, v in data.items() if k != "createdAt"}
        return cls(data)


class CrossmintWalletClient(WalletClientInterface):
    """Crossmint wallet implementation."""

    def __init__(
        self,
        web3: Web3,
        api_key: str,
        wallet_locator: Optional[str] = None,
    ):
        self.web3 = web3
        self.api_key = api_key
        self.base_url = "https://staging.crossmint.com/api/2022-06-09"

        # Handle wallet based on locator
        if wallet_locator is None:
            # Create a new wallet if wallet_locator is not provided
            wallet_info = self._create_wallet()
            self.wallet = CrossmintWallet.from_dict(wallet_info)
        else:
            # Retrieve wallet data using the provided locator
            wallet_info = self._get_wallet_by_locator(wallet_locator)
            self.wallet = CrossmintWallet.from_dict(wallet_info)

        # Verify we have an address
        if not self.wallet.address:
            raise AgentKitError("Crossmint wallet has no address")

        self.address = self.wallet.address

    def _get_wallet_by_locator(self, wallet_locator: str) -> Dict:
        """Retrieve wallet data from Crossmint API using wallet locator."""
        try:
            response = requests.get(
                f"{self.base_url}/wallets/{wallet_locator}",
                headers={
                    "X-API-KEY": self.api_key,
                    "Accept": "application/json",
                },
                timeout=30,
            )

            # Handle response based on status code
            if response.status_code == 200:
                print(response.json())
                return response.json()
            else:
                error_message = f"Failed to retrieve Crossmint wallet: Status {response.status_code}"
                try:
                    error_detail = response.json()
                    error_message += f", Details: {error_detail}"
                except:
                    error_message += f", Response: {response.text}"

                raise AgentKitError(error_message)

        except requests.exceptions.RequestException as e:
            raise AgentKitError(f"Request to Crossmint API failed: {str(e)}")

    def _create_wallet(self) -> Dict:
        """Create a new Crossmint wallet."""
        payload = {
            "type": "evm-smart-wallet",
            "config": {"adminSigner": {"type": "evm-fireblocks-custodial"}},
        }

        try:
            response = requests.post(
                f"{self.base_url}/wallets",
                headers={
                    "X-API-KEY": self.api_key,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                json=payload,
                timeout=30,
            )

            # Handle response based on status code
            if response.status_code in (200, 201):
                return response.json()
            else:
                error_message = (
                    f"Failed to create Crossmint wallet: Status {response.status_code}"
                )
                try:
                    error_detail = response.json()
                    error_message += f", Details: {error_detail}"
                except:
                    error_message += f", Response: {response.text}"

                raise AgentKitError(error_message)

        except requests.exceptions.RequestException as e:
            raise AgentKitError(f"Request to Crossmint API failed: {str(e)}")

    def get_address(self) -> str:
        return self.address

    def sign_message(self, message: str) -> Dict[str, str]:
        payload = {"message": message, "encoding": "utf8"}
        response = requests.post(
            f"{self.base_url}/wallets/{self.wallet.address}/sign",
            headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
            json=payload,
        )
        if response.status_code != 200:
            raise AgentKitError(
                f"Failed to sign message with Crossmint: {response.text}"
            )
        result = response.json()
        return {"signature": result.get("signature", "")}

    def balance_of(self, address: Optional[str] = None) -> Dict:
        if not address:
            address = self.wallet.address

        # First try to get balance via Crossmint API
        try:
            response = requests.get(
                f"{self.base_url}/wallets/{self.wallet.address}/balances",
                headers={"X-API-KEY": self.api_key},
            )
            if response.status_code == 200:
                balances = response.json()
                native_token = next(
                    (b for b in balances if b.get("type") == "NATIVE"), None
                )
                if native_token:
                    return {
                        "decimals": 18,
                        "symbol": "ETH",  # This will be the native token of the chain
                        "value": str(
                            Web3.from_wei(int(native_token.get("balance", 0)), "ether")
                        ),
                        "in_base_units": str(native_token.get("balance", 0)),
                    }
        except Exception as e:
            logger.warning(f"Failed to get balance from Crossmint API: {e}")

        # Fallback to Web3 if Crossmint API fails
        balance_wei = self.web3.eth.get_balance(address)
        return {
            "decimals": 18,
            "symbol": "ETH",
            "value": str(Web3.from_wei(balance_wei, "ether")),
            "in_base_units": str(balance_wei),
        }

    def send_transaction(self, transaction: EVMTransaction) -> Dict[str, str]:
        payload = {
            "to": transaction.to,
            "value": str(transaction.value),
            "data": transaction.data,
        }

        if transaction.gas:
            payload["gasLimit"] = str(transaction.gas)

        response = requests.post(
            f"{self.base_url}/wallets/{self.wallet.address}/transactions",
            headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
            json=payload,
        )

        if response.status_code != 202:
            raise AgentKitError(
                f"Failed to send transaction via Crossmint: {response.text}"
            )

        result = response.json()
        tx_hash = result.get("txHash")

        if not tx_hash:
            raise AgentKitError("No transaction hash returned from Crossmint")

        # Wait for transaction receipt
        self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return {"hash": tx_hash}
