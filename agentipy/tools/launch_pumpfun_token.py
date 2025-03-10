import json
import logging
from typing import Any, Dict, Optional

import aiohttp
import requests
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.commitment_config import CommitmentLevel  # type: ignore
from solders.keypair import Keypair  # type: ignore
from solders.message import to_bytes_versioned  # type: ignore
from solders.rpc.config import RpcSendTransactionConfig  # type: ignore
from solders.rpc.requests import SendVersionedTransaction  # type: ignore
from solders.transaction import VersionedTransaction  # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.constants import DEFAULT_OPTIONS
from agentipy.helpers import fix_asyncio_for_windows
from agentipy.types import PumpfunTokenOptions, TokenLaunchResult
from agentipy.utils.send_tx import sign_and_send_transaction

logger = logging.getLogger(__name__)

fix_asyncio_for_windows()

class PumpfunTokenManager:
    @staticmethod
    async def _upload_metadata(
        session: aiohttp.ClientSession,
        token_name: str,
        token_ticker: str,
        description: str,
        image_url: str,
        options: Optional[PumpfunTokenOptions] = None
    ) -> Dict[str, Any]:
        """
        Uploads token metadata and image to IPFS via Pump.fun.

        Args:
            session: An active aiohttp.ClientSession object
            token_name: Name of the token
            token_ticker: Token symbol/ticker
            description: Token description
            image_url: URL of the token image
            options: Optional token configuration

        Returns:
            A dictionary containing the metadata response from the server.
        """
        logger.debug("Preparing form data for IPFS upload...")
        form_data = aiohttp.FormData()
        form_data.add_field("name", token_name)
        form_data.add_field("symbol", token_ticker)
        form_data.add_field("description", description)
        form_data.add_field("showName", "true")

        if options:
            if options.twitter:
                form_data.add_field("twitter", options.twitter)
            if options.telegram:
                form_data.add_field("telegram", options.telegram)
            if options.website:
                form_data.add_field("website", options.website)

        logger.debug(f"Downloading image from {image_url}...")
        async with session.get(image_url) as image_response:
            if image_response.status != 200:
                raise ValueError(f"Failed to download image from {image_url} (status {image_response.status})")
            image_data = await image_response.read()

        form_data.add_field(
            "file",
            image_data,
            filename="token_image.png",
            content_type="image/png"
        )

        logger.debug("Uploading metadata to Pump.fun IPFS endpoint...")
        async with session.post("https://pump.fun/api/ipfs", data=form_data) as response:
            if response.status != 200:
                error_text = await response.text()
                raise RuntimeError(f"Metadata upload failed (status {response.status}): {error_text}")

            return await response.json()

    @staticmethod
    async def _create_token_transaction(
        session: aiohttp.ClientSession,
        agent: SolanaAgentKit,
        mint_keypair: Keypair,
        metadata_response: Dict[str, Any],
        options: Optional[PumpfunTokenOptions] = None
    ) -> VersionedTransaction:
        """
        Creates a token transaction via the Pump.fun API.

        Args:
            session: An active aiohttp.ClientSession object
            agent: SolanaAgentKit instance
            mint_keypair: The Keypair for the token mint
            metadata_response: The response from the metadata upload
            options: Optional token configuration

        Returns:
            Serialized transaction bytes.
        """
        options = options or PumpfunTokenOptions()

        payload = {
            "publicKey": str(agent.wallet_address),
            "action": "create",
            "tokenMetadata": {
                "name": metadata_response["metadata"]["name"],
                "symbol": metadata_response["metadata"]["symbol"],
                "uri": metadata_response["metadataUri"],
            },
            "mint": str(mint_keypair.pubkey()),
            "denominatedInSol": "true",
            "amount": options.initial_liquidity_sol,
            "slippage": options.slippage_bps,
            "priorityFee": options.priority_fee,
            "pool": "pump"
        }

        logger.debug("Requesting token transaction from Pump.fun...")
        response = requests.post(
                "https://pumpportal.fun/api/trade-local",
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )

        if response.status_code != 200:
            raise RuntimeError(
                f"Transaction creation failed (status {response.status_code}): {response.text}"
            )

        tx_data = response.content

        tx = VersionedTransaction.from_bytes(tx_data)
        logger.debug(f"Transaction successfully created: {tx}")
        return tx

    @staticmethod
    async def launch_pumpfun_token(
        agent: SolanaAgentKit,
        token_name: str,
        token_ticker: str,
        description: str,
        image_url: str,
        options: Optional[PumpfunTokenOptions] = None
    ) -> TokenLaunchResult:
        """
        Launches a new token on Pump.fun.

        Args:
            agent: SolanaAgentKit instance
            token_name: Name of the token
            token_ticker: Token symbol/ticker
            description: Token description
            image_url: URL of the token image
            options: Optional token configuration

        Returns:
            TokenLaunchResult containing the transaction signature, mint address, and metadata URI.
        """
        logger.info("Starting token launch process...")
        mint_keypair = Keypair()
        logger.info(f"Mint public key: {mint_keypair.pubkey()}")

        try:
            # Use a single aiohttp session for both metadata upload and transaction creation
            async with aiohttp.ClientSession() as session:
                logger.info("Uploading metadata to IPFS...")
                metadata_response = await PumpfunTokenManager._upload_metadata(
                    session,
                    token_name,
                    token_ticker,
                    description,
                    image_url,
                    options
                )
                logger.debug(f"Metadata response: {metadata_response}")

                logger.info("Creating token transaction...")
                tx_data = await PumpfunTokenManager._create_token_transaction(
                    session,
                    agent,
                    mint_keypair,
                    metadata_response,
                    options
                )
                logger.debug(f"Deserializing transaction...")
                tx = VersionedTransaction(tx_data.message, [mint_keypair, agent.wallet])


            lcommitment = CommitmentLevel.Confirmed
            config = RpcSendTransactionConfig(preflight_commitment=lcommitment)
            txPayload = SendVersionedTransaction(tx, config)


            logger.info("Sending transaction to Solana network...")

            response = requests.post(
            url= agent.rpc_url,
            headers={"Content-Type": "application/json"},
            data=SendVersionedTransaction(tx, config).to_json()
            )
            if response.status_code != 200:
                raise RuntimeError(f"Failed to send transaction: {response.text}")

            print(f"response: {response.json()}")

            txSignature = response.json()['result']
            if not txSignature:
                raise RuntimeError("Transaction signature not found in response.")
            logger.info(f'Transaction: https://solscan.io/tx/{txSignature}')
            return TokenLaunchResult(
                signature=txSignature,
                mint=str(mint_keypair.pubkey()),
                metadata_uri=metadata_response["metadataUri"]
            )

        except Exception as error:
            logger.error(f"Error in launch_pumpfun_token: {error}")
            raise
