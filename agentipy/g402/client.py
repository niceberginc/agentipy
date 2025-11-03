import os
from dotenv import load_dotenv
from solders.keypair import Keypair
from g402_cl.buyer_sdk import SolanaPaymentClient

load_dotenv()
SERVER_URL = "http://127.0.0.1:8000/premium-data"
RPC_URL = "https://api.devnet.solana.com"

secret_b58 = os.getenv("CLIENT_WALLET_PRIVATE_KEY_BASE58")
if not secret_b58:
    raise SystemExit("Error: Set CLIENT_WALLET_PRIVATE_KEY_BASE58 in your .env file")

client_keypair = Keypair.from_base58_string(secret_b58)

if __name__ == "__main__":
    payment_client = SolanaPaymentClient(
        rpc_url=RPC_URL,
        client_keypair=client_keypair
    )

    payment_client.get_premium_data(server_url=SERVER_URL)