from typing import Dict, Optional

from eth_account.messages import encode_defunct
from eth_typing import HexStr
from eth_utils.address import to_checksum_address
from web3 import Web3
from web3.types import TxParams, Wei


class EVMTransaction:
    """Transaction parameters for EVM."""

    def __init__(
        self, to: str, value: int = 0, data: str = "", gas: Optional[int] = None
    ):
        self.to = to_checksum_address(to)
        self.value = Wei(value)
        self.data = HexStr(data)
        self.gas = gas


class WalletClientInterface:
    """Interface defining the required methods for a wallet client."""

    def get_address(self) -> str:
        raise NotImplementedError()

    def sign_message(self, message: str) -> Dict[str, str]:
        raise NotImplementedError()

    def balance_of(self, address: str) -> Dict:
        raise NotImplementedError()

    def send_transaction(self, transaction: EVMTransaction) -> Dict[str, str]:
        raise NotImplementedError()


class EVMWalletClient(WalletClientInterface):
    """EVM wallet implementation."""

    def __init__(self, web3: Web3, private_key: str):
        self.web3 = web3
        self.account = web3.eth.account.from_key(private_key)

    def get_address(self) -> str:
        return self.account.address

    def sign_message(self, message: str) -> Dict[str, str]:
        message_bytes = encode_defunct(text=message)
        signed = self.web3.eth.account.sign_message(
            message_bytes, private_key=self.account.key
        )
        return {"signature": signed.signature.hex()}

    def balance_of(self, address: Optional[str] = None) -> Dict:
        if not address:
            address = self.wallet.address
        balance_wei = self.web3.eth.get_balance(to_checksum_address(address))
        return {
            "decimals": 18,
            "symbol": "ETH",
            "value": str(Web3.from_wei(balance_wei, "ether")),
            "in_base_units": str(balance_wei),
        }

    def send_transaction(self, transaction: EVMTransaction) -> Dict[str, str]:
        tx_params: TxParams = {
            "from": self.account.address,
            "to": transaction.to,
            "value": transaction.value,
            "data": transaction.data,
            "chainId": self.web3.eth.chain_id,
            "nonce": self.web3.eth.get_transaction_count(self.account.address),
        }

        if transaction.gas:
            tx_params["gas"] = transaction.gas
        else:
            tx_params["gas"] = self.web3.eth.estimate_gas(tx_params)

        signed_tx = self.web3.eth.account.sign_transaction(
            tx_params, private_key=self.account.key
        )
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return {"hash": tx_hash.hex()}
