import os
from fastapi import FastAPI, Request, status, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from g402_cl.seller_sdk import SolanaPaymentGuard

load_dotenv()
SERVER_WALLET_ADDRESS = os.getenv("SERVER_WALLET_ADDRESS")
if not SERVER_WALLET_ADDRESS:
    raise ValueError("Set SERVER_WALLET_ADDRESS in .env")

SOLANA_RPC_URL = "https://api.devnet.solana.com"
PREMIUM_PRICE_LAMPORTS = 10_000

guard = SolanaPaymentGuard(
    rpc_url=SOLANA_RPC_URL,
    server_wallet=SERVER_WALLET_ADDRESS,
    price_lamports=PREMIUM_PRICE_LAMPORTS
)

app = FastAPI(title="G402 Solana Server")

@app.get("/")
def root():
    return {"status": "ok", "message": "This is a free endpoint. Try /premium-data"}

@app.get("/premium-data")
async def premium_data(request: Request):
    try:
        payment_info = await guard.require_payment(request)
        
        if isinstance(payment_info, Response):
            return payment_info

        return {
            "message": "Payment accepted! Here is your premium data.",
            "data": "The secret to the universe is 42.",
            "payment_details": payment_info
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Payment verification failed", "details": str(e)}
        )