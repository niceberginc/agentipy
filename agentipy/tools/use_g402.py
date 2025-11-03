
import time
import httpx
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.system_program import TransferParams, transfer
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solders.compute_budget import set_compute_unit_price
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed, Finalized
from agentipy.agent import SolanaAgentKit

class G402DataFetcher:
    @staticmethod
    async def _confirm_transaction(agent: SolanaAgentKit, sig_str: str, timeout: int = 60):
        print(f"Waiting for confirmation of tx: {sig_str} (timeout: {timeout}s)...")
        try:
            signature = Signature.from_string(sig_str)
            resp = await agent.connection.confirm_transaction(
                signature, commitment=Finalized, sleep_seconds=2
            )
            if resp.value[0].err:
                raise SystemExit(f"Transaction failed on-chain: {resp.value[0].err}")
            print("Transaction Confirmed!")
            return True
        except Exception as e:
            explorer_url = f"https://explorer.solana.com/tx/{sig_str}?cluster=devnet"
            print(f"An error occurred during confirmation: {e}")
            raise SystemExit(f"Tx confirmation failed or timed out: {explorer_url}")

    @staticmethod
    async def _send_payment(agent: SolanaAgentKit, to_addr: str, lamports: int) -> str:
        print(f"Paying {lamports / 1_000_000_000:.6f} SOL to {to_addr[:8]}...")
        blockhash_resp = await agent.connection.get_latest_blockhash(commitment=Confirmed)
        recent_blockhash = blockhash_resp.value.blockhash
        priority_ix = set_compute_unit_price(200_000)
        transfer_ix = transfer(TransferParams(
            from_pubkey=agent.wallet.pubkey(),
            to_pubkey=Pubkey.from_string(to_addr),
            lamports=lamports
        ))
        msg = MessageV0.try_compile(
            payer=agent.wallet.pubkey(),
            instructions=[priority_ix, transfer_ix],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash
        )
        tx = VersionedTransaction(msg, [agent.wallet])
        opts = TxOpts(skip_preflight=False, preflight_commitment=Confirmed)
        sig_resp = await agent.connection.send_transaction(tx, opts)
        sig_str = str(sig_resp.value)
        print(f"Payment sent! Signature: {sig_str}")
        await G402DataFetcher._confirm_transaction(agent, sig_str)
        return sig_str

    @staticmethod
    async def fetch_premium_data(agent: SolanaAgentKit, url: str):
        async with httpx.AsyncClient(timeout=20.0) as session:
            print(f"STEP 1: Agent requesting data from {url} (expecting 402)...")
            try:
                initial_response = await session.get(url)
            except httpx.RequestError as e:
                raise SystemExit(f"Connection error: {e}")
            if initial_response.status_code != 402:
                raise SystemExit(f"Unexpected status: {initial_response.status_code}\n{initial_response.text}")

            details = initial_response.json()
            print("Received 402. Payment Details:", details)

            print("STEP 2: Agent sending payment on Solana devnet...")
            tx_sig = await G402DataFetcher._send_payment(agent, details["receiver"], details["amount_lamports"])

            print("STEP 3: Agent retrying request with payment proof...")
            session.headers.update({"X-Payment-Signature": tx_sig, "X-Payment-Reference": details["reference"]})
            final_response = await session.get(url)

            print(f"FINAL RESPONSE ({final_response.status_code}):")
            final_data = final_response.json()
            print(final_data)

            if final_response.status_code == 200:
                print("SUCCESS! Agent unlocked the premium data!")
            else:
                print("Server rejected agent's payment proof. Check server logs.")

            return final_data