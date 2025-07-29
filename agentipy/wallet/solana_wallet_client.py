from typing import Dict, List, Optional

import nacl.signing
from solana.rpc.api import Client as SolanaClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solana.transaction import Transaction  # type: ignore
from solders.instruction import Instruction  # type: ignore
from solders.keypair import Keypair  # type: ignore
from solders.pubkey import Pubkey  # type: ignore

from .base_wallet_client import BaseWalletClient


class SolanaTransaction:
    """Transaction parameters for Solana."""

    def __init__(
        self,
        instructions: List[Instruction],
        accounts_to_sign: Optional[List[Keypair]] = None,
    ):
        self.instructions = instructions
        self.accounts_to_sign = accounts_to_sign


class SolanaWalletClient(BaseWalletClient):
    """Solana wallet implementation."""

    def __init__(self, client: SolanaClient, keypair: Keypair):
        self.client = client
        self.keypair = keypair

    def get_address(self) -> str:
        return str(self.keypair.pubkey())

    def sign_message(self, message: str) -> Dict[str, str]:
        message_bytes = message.encode("utf-8")
        signed = nacl.signing.SigningKey(self.keypair.secret()).sign(message_bytes)
        return {"signature": signed.signature.hex()}

    def balance_of(self, address: str) -> Dict:
        pubkey = Pubkey.from_string(address)
        balance_lamports = self.client.get_balance(pubkey).value
        return {
            "decimals": 9,
            "symbol": "SOL",
            "value": str(balance_lamports / 10**9),
            "in_base_units": str(balance_lamports),
        }

    async def send_transaction(self, transaction: SolanaTransaction) -> Dict[str, str]:
        recent_blockhash = self.client.get_latest_blockhash().value.blockhash
        tx = Transaction()
        tx.recent_blockhash = recent_blockhash
        tx.fee_payer = self.keypair.pubkey()

        for instruction in transaction.instructions:
            tx.add(instruction)

        signers = [self.keypair]
        if transaction.accounts_to_sign:
            signers.extend(transaction.accounts_to_sign)

        tx.sign(*signers)
        # Check if client has async methods
        if hasattr(self.client, "send_transaction_async"):
            result = await self.client.send_transaction_async(
                tx,
                opts=TxOpts(
                    skip_preflight=False, max_retries=10, preflight_commitment=Confirmed
                ),
            )
            await self.client.confirm_transtion_async(
                result.value, commitment=Confirmed
            )
        else:
            result = self.client.send_transaction(
                tx.serialize(),
                opts=TxOpts(
                    skip_preflight=False, max_retries=10, preflight_commitment=Confirmed
                ),
            )
            self.client.confirm_transaction(result.value, commitment=Confirmed)
        return {"hash": str(result.value)}
