# g402_cl/buyer_sdk.py

import time
import requests
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.system_program import TransferParams, transfer
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solders.compute_budget import set_compute_unit_price
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed, Finalized # Import Finalized

class SolanaPaymentClient:
    def __init__(self, rpc_url: str, client_keypair: Keypair):
        self.client = Client(rpc_url, timeout=30.0)
        self.keypair = client_keypair
        print("✅ Buyer SDK: SolanaPaymentClient initialized.")
        print(f"   - Pubkey: {self.keypair.pubkey()}")
        try:
            bal = self.client.get_balance(self.keypair.pubkey()).value
            print(f"   - Balance: {bal / 1_000_000_000:.9f} SOL")
        except Exception as e:
            print(f"⚠️  Could not fetch wallet balance. Check RPC connection. Error: {e}")

    def _wait_for_confirmation(self, sig: str, timeout: int = 60):
        """Robust confirmation waiting using client.confirm_transaction"""
        print(f"Waiting for confirmation of tx: {sig} (timeout: {timeout}s)...")
        try:
            signature_to_check = Signature.from_string(sig)
            # Use the library's built-in confirmation function
            confirmation_resp = self.client.confirm_transaction(
                signature_to_check,
                commitment=Finalized,  # Wait for finalization for higher certainty
                sleep_seconds=2,  # How long to wait between checks
                last_valid_block_height=self.client.get_latest_blockhash().value.last_valid_block_height
            )
            if confirmation_resp.value[0].err:
                raise SystemExit(f"❌ Transaction failed: {confirmation_resp.value[0].err}")

            print("✅ Transaction Confirmed!")
            return True

        except Exception as e:
            explorer_url = f"https://explorer.solana.com/tx/{sig}?cluster=devnet"
            print(f"An error occurred during confirmation: {e}")
            raise SystemExit(f"❌ Tx confirmation failed or timed out: {explorer_url}")


    def _send_payment(self, to_addr: str, lamports: int) -> str:
        print(f"   → Paying {lamports / 1_000_000_000:.6f} SOL → {to_addr[:8]}...")

        # 1. FRESH blockhash (critical!)
        blockhash_resp = self.client.get_latest_blockhash(commitment=Confirmed)
        recent_blockhash = blockhash_resp.value.blockhash

        # 2. Priority fee: 200k micro-lamports = lands in <5s on Devnet
        priority_ix = set_compute_unit_price(200_000)

        # 3. Transfer
        transfer_ix = transfer(TransferParams(
            from_pubkey=self.keypair.pubkey(),
            to_pubkey=Pubkey.from_string(to_addr),
            lamports=lamports
        ))

        # 4. Build message
        msg = MessageV0.try_compile(
            payer=self.keypair.pubkey(),
            instructions=[priority_ix, transfer_ix],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash,
        )

        tx = VersionedTransaction(msg, [self.keypair])
        raw_tx = bytes(tx)

        # 5. Send with preflight + retry
        opts = TxOpts(skip_preflight=False, preflight_commitment=Confirmed)
        sig = self.client.send_raw_transaction(raw_tx, opts).value

        print(f"   Payment sent! Signature: {sig}")
        self._wait_for_confirmation(str(sig))
        return str(sig)

    def get_premium_data(self, server_url: str):
        """Main method: Get 402 → Pay → Retry with proof"""
        session = requests.Session()
        print(f"\n{'='*60}")
        print(f"STEP 1: Requesting data from {server_url} (expecting 402)...")
        print(f"{'='*60}")

        try:
            initial_response = session.get(server_url, timeout=10)
        except requests.exceptions.RequestException as e:
            raise SystemExit(f"❌ Connection error: {e}")

        if initial_response.status_code != 402:
            raise SystemExit(
                f"❌ Unexpected status: {initial_response.status_code}\n"
                f"{initial_response.text}"
            )

        details = initial_response.json()
        print("✅ Received 402. Payment Details:", details)

        print(f"\n{'='*60}")
        print("STEP 2: Sending payment on Solana devnet...")
        print(f"{'='*60}")
        tx_sig = self._send_payment(
            details["receiver"],
            details["amount_lamports"]
        )

        print(f"\n{'='*60}")
        print("STEP 3: Retrying request with payment proof...")
        print(f"{'='*60}")

        session.headers.update({
            "X-Payment-Signature": tx_sig,
            "X-Payment-Reference": details["reference"],
        })

        final_response = session.get(server_url, timeout=10)
        print(f"\n🎉 FINAL RESPONSE ({final_response.status_code}):")
        print(final_response.json())
        print(f"{'='*60}")

        if final_response.status_code == 200:
            print("🚀 SUCCESS! Payment accepted, premium data unlocked!")
        else:
            print("⚠️  Server rejected payment proof. Check server logs.")

        return final_response.json()