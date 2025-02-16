import base64
from typing import Optional

import nacl.encoding
import nacl.signing
import requests
from solders.keypair import Keypair  # type: ignore

from agentipy.agent import SolanaAgentKit


class CybersManager:
    API_BASE_URL = "https://api.cybers.app/v1"

    @staticmethod
    def _sign_message(keypair: Keypair, message: str) -> str:
        """
        Sign a message with the wallet's private key.

        Args:
            keypair (Keypair): The wallet keypair.
            message (str): The message to sign.

        Returns:
            str: Base58-encoded signature.
        """
        message_bytes = message.encode("utf-8")
        signing_key = nacl.signing.SigningKey(keypair.secret()[:32])
        signature = signing_key.sign(message_bytes).signature
        return base64.b58encode(signature).decode("utf-8")

    @staticmethod
    def authenticate_wallet(agent: SolanaAgentKit) -> Optional[str]:
        """
        Authenticate with Cybers API and retrieve JWT token.

        Args:
            agent (SolanaAgentKit): The Solana agent containing the wallet keypair.

        Returns:
            Optional[str]: JWT token if authentication is successful.
        """
        try:
            keypair = agent.wallet
            wallet_address = str(keypair.pubkey())
            message = "Sign in to Cyber"

            signature = CybersManager._sign_message(keypair, message)

            response = requests.post(
                f"{CybersManager.API_BASE_URL}/auth/verify-signature",
                json={"walletAddress": wallet_address, "signature": signature, "message": message},
            )

            if response.status_code == 200:
                return response.json().get("token")
            else:
                raise Exception(f"Authentication failed: {response.text}")
        except Exception as e:
            raise Exception(f"Error during wallet authentication: {str(e)}")

    @staticmethod
    def create_coin(
        agent: SolanaAgentKit,
        name: str,
        symbol: str,
        image_path: str,
        tweet_author_id: str,
        tweet_author_username: str,
    ) -> dict:
        """
        Create a coin on Cybers.

        Args:
            agent (SolanaAgentKit): The Solana agent containing the wallet keypair.
            name (str): Name of the token.
            symbol (str): Symbol of the token.
            image_path (str): Path to the token image.
            tweet_author_id (str): Twitter user ID of the token creator.
            tweet_author_username (str): Twitter username of the token creator.

        Returns:
            dict: Response containing the mint address if successful.
        """
        try:
            jwt_token = CybersManager.authenticate_wallet(agent)
            if not jwt_token:
                raise Exception("Failed to retrieve JWT token.")

            name = name[:64]
            symbol = symbol[:10]

            with open(image_path, "rb") as image_file:
                image_data = image_file.read()

            files = {
                "image": ("token_image.jpg", image_data, "image/jpeg"),
            }
            data = {
                "name": name,
                "symbol": symbol,
                "description": f"AI Agent {name} token.",
                "personality": "Friendly and helpful",
                "instruction": "Respond politely to all queries about the token",
                "knowledge": "Basic cryptocurrency knowledge",
                "twitter": symbol.lower(),
                "telegram": f"{symbol.lower()}_group",
                "website": f"https://{symbol.lower()}.com",
                "creatorTwitterUserId": tweet_author_id,
                "creatorTwitterUsername": tweet_author_username,
            }

            response = requests.post(
                f"{CybersManager.API_BASE_URL}/coin/create",
                headers={"Authorization": f"Bearer {jwt_token}"},
                files=files,
                data=data,
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to create coin: {response.text}")

        except Exception as e:
            raise Exception(f"Error creating coin: {str(e)}")
