import time
import uuid
import json
from fastapi import Request, status, Response
from fastapi.responses import JSONResponse
from solders.signature import Signature
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed
from solana.exceptions import SolanaRpcException

processed_references = set()

class SolanaPaymentGuard:
    def __init__(self, rpc_url: str, server_wallet: str, price_lamports: int):
        self.client = Client(rpc_url)
        self.server_wallet = server_wallet
        self.price_lamports = price_lamports
        print("Seller SDK: SolanaPaymentGuard initialized.")

    def _find_system_transfer(self, tx_info: dict):
        try:
            transaction_data = tx_info.get('transaction', {})
            msg = transaction_data.get('message', {})
            instructions = msg.get('instructions', [])
            for ix in instructions:
                if ix.get("program") == "system" and ix.get("parsed", {}).get("type") == "transfer":
                    info = ix.get("parsed", {}).get("info", {})
                    destination = info.get("destination")
                    lamports = info.get("lamports")
                    if destination and lamports is not None:
                        return destination, lamports
        except Exception as e:
            print(f"Error parsing transaction: {e}")
        return None, 0

    async def require_payment(self, request: Request):
        sig_header = request.headers.get("X-Payment-Signature")
        ref_header = request.headers.get("X-Payment-Reference")

        if not sig_header or not ref_header:
            reference = str(uuid.uuid4())
            return JSONResponse(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                content={
                    "message": "Payment Required",
                    "receiver": self.server_wallet,
                    "amount_lamports": self.price_lamports,
                    "reference": reference,
                },
            )

        if ref_header in processed_references:
            raise ValueError("This payment reference has already been used.")

        sig = Signature.from_string(sig_header.strip())
        
        tx_info = None
        for attempt in range(5):
            try:
                resp = self.client.get_transaction(
                    sig, "jsonParsed", max_supported_transaction_version=0, commitment=Confirmed
                )
                if resp.value:
                    tx_info = resp.value
                    break
            except SolanaRpcException as e:
                print(f"RPC error on attempt {attempt+1}: {e}")
            time.sleep(2)

        if not tx_info:
            raise ValueError("Transaction not found or not confirmed.")

        if tx_info.transaction.meta and tx_info.transaction.meta.err:
            raise ValueError(f"Transaction failed on-chain: {tx_info.transaction.meta.err}")

        tx_info_dict = json.loads(tx_info.to_json())
        to_addr, lamports = self._find_system_transfer(tx_info_dict)

        if to_addr != self.server_wallet:
            raise ValueError(f"Payment sent to wrong receiver. Expected {self.server_wallet}, got {to_addr}.")
        if lamports < self.price_lamports:
            raise ValueError(f"Insufficient amount paid. Expected {self.price_lamports}, got {lamports}.")

        processed_references.add(ref_header)
        print(f"SDK: Payment verified for {lamports} lamports. Signature: {sig}")
        return {"signature": str(sig), "amount": lamports}