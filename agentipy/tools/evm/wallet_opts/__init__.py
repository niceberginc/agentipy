from typing import Dict, Optional

from eth_account import Account
from eth_account.messages import encode_defunct, encode_typed_data
from eth_typing import ChecksumAddress, HexStr
from eth_utils.address import to_checksum_address
from web3 import Web3
from web3.types import TxParams, Wei


class Web3EVMClient:
    def __init__(self, web3: Web3, private_key: str):
        self._web3 = web3
        self._private_key = private_key
        self._account = Account.from_key(private_key)  # Derive account from private key
        self._address = self._account.address

    def get_address(self) -> str:
        """Return the derived account address."""
        return self._address

    def resolve_address(self, address: str) -> ChecksumAddress:
        """Resolve an address to its canonical form."""
        if Web3.is_address(address):
            return to_checksum_address(address)

        try:
            resolved = self._web3.ens.address(address)  # type: ignore
            if not resolved:
                raise ValueError("ENS name could not be resolved")
            return to_checksum_address(resolved)
        except Exception as e:
            raise ValueError(f"Failed to resolve ENS name: {str(e)}")

    def sign_message(self, message: str) -> HexStr:
        """Sign a message with the private key using EIP-191 encoding."""
        message_encoded = encode_defunct(text=message)  # Correctly format the message
        signature = Account.sign_message(message_encoded, self._private_key)
        return signature.signature.hex()

    def sign_typed_data(self, data: dict) -> HexStr:
        """Sign typed data according to EIP-712."""
        if "chainId" in data["domain"]:
            data["domain"]["chainId"] = int(data["domain"]["chainId"])

        structured_data = encode_typed_data(full_message=data)  # type: ignore
        signature = Account.sign_message(structured_data, self._private_key)
        return signature.signature.hex()

    def send_transaction(self, transaction: dict) -> Dict[str, str]:
        """Sign and send a transaction using the private key."""
        to_address = self.resolve_address(transaction["to"])

        tx_params: TxParams = {
            "from": self._address,
            "to": to_checksum_address(to_address),
            "value": Wei(transaction.get("value", 0)),
            "gas": transaction.get("gas", 21000),
            "gasPrice": self._web3.eth.gas_price,
            "nonce": self._web3.eth.get_transaction_count(self._address),
        }

        signed_tx = self._web3.eth.account.sign_transaction(tx_params, self._private_key)
        tx_hash = self._web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self._wait_for_receipt(HexStr(tx_hash.hex()))

    def balance_of(self, address: str) -> Dict[str, str]:
        """Get the balance of an address."""
        resolved_address = self.resolve_address(address)
        balance_wei = self._web3.eth.get_balance(resolved_address)

        return {
            "value": Web3.from_wei(balance_wei, "ether"),
            "in_base_units": str(balance_wei),
        }

    def _wait_for_receipt(self, tx_hash: HexStr) -> Dict[str, str]:
        """Wait for a transaction receipt and return standardized result."""
        receipt = self._web3.eth.wait_for_transaction_receipt(tx_hash)
        return {
            "hash": receipt["transactionHash"].hex(),
            "status": "1" if receipt["status"] == 1 else "0",
        }

def web3_client(client: Web3, private_key: str) -> Web3EVMClient:
    """Create a new Web3EVMClient instance with a private key."""
    return Web3EVMClient(client, private_key)
