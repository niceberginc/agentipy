from typing import Dict, Optional

from eth_account.messages import encode_typed_data
from eth_typing import ChecksumAddress, HexStr
from eth_utils.address import to_checksum_address
from web3 import Web3
from web3.types import TxParams, Wei


class Web3EVMClient:
    def __init__(self, web3: Web3):
        self._web3 = web3

    def get_address(self) -> str:
        """Get the default account address."""
        if not self._web3.eth.default_account:
            return ""
        return self._web3.eth.default_account

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
        """Sign a message with the current account."""
        if not self._web3.eth.default_account:
            raise ValueError("No account connected")

        signature = self._web3.eth.sign(self._web3.eth.default_account, text=message)
        return signature.hex()

    def sign_typed_data(self, data: dict) -> HexStr:
        """Sign typed data according to EIP-712."""
        if not self._web3.eth.default_account:
            raise ValueError("No account connected")

        if "chainId" in data["domain"]:
            data["domain"]["chainId"] = int(data["domain"]["chainId"])

        structured_data = encode_typed_data(full_message=data)  # type: ignore
        signature = self._web3.eth.sign(self._web3.eth.default_account, structured_data)
        return signature.hex()

    def send_transaction(self, transaction: dict) -> Dict[str, str]:
        """Send a transaction on the EVM chain."""
        if not self._web3.eth.default_account:
            raise ValueError("No account connected")

        to_address = self.resolve_address(transaction["to"])

        tx_params: TxParams = {
            "from": self._web3.eth.default_account,
            "to": to_checksum_address(to_address),
            "value": Wei(transaction.get("value", 0)),
        }

        tx_hash = self._web3.eth.send_transaction(tx_params)
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

def web3(client: Web3) -> Web3EVMClient:
    """Create a new Web3EVMClient instance."""
    return Web3EVMClient(client)
