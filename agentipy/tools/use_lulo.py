import base64
import json

import aiohttp
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.message import to_bytes_versioned  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solders.transaction import VersionedTransaction  # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.constants import FLEXLEND_BASE_URL
from agentipy.helpers import fix_asyncio_for_windows
from agentipy.wallet.privy_wallet_client import PrivyWalletClient
from agentipy.wallet.solana_wallet_client import SolanaWalletClient

fix_asyncio_for_windows()


class LuloManager:
    BASE_URL = FLEXLEND_BASE_URL

    @staticmethod
    async def lend_asset(agent: SolanaAgentKit, amount: float) -> str:
        """
        Lend tokens for yields using Lulo API.

        Args:
            agent (SolanaAgentKit): SolanaAgentKit instance with connection and wallet.
            amount (float): Amount of USDC to lend.

        Returns:
            str: Transaction signature.
        """
        try:
            url = f"https://blink.lulo.fi/actions?amount={amount}&symbol=USDC"
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({"account": str(agent.wallet_address if isinstance(agent.wallet_client, PrivyWalletClient) else agent.wallet.pubkey())})

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    if response.status != 200:
                        raise Exception(f"Lulo API Error: {response.status}")
                    data = await response.json()

            transaction_bytes = base64.b64decode(data["transaction"])
            lulo_txn = VersionedTransaction.from_bytes(transaction_bytes)

            latest_blockhash = await agent.connection.get_latest_blockhash()

            if isinstance(agent.wallet_client, PrivyWalletClient):
                res = await agent.wallet_client.send_transaction(data["transaction"])
                tx_id = res.get("hash", "tx_id")
                signature = tx_id
            elif isinstance(agent.wallet_client, SolanaWalletClient):
                signature = agent.wallet.sign_message(to_bytes_versioned(lulo_txn.message))
                signed_tx = VersionedTransaction.populate(lulo_txn.message, [signature])
                tx_resp = await agent.connection.send_transaction(
                    signed_tx,
                    opts=TxOpts(preflight_commitment=Confirmed)
                )
                tx_id = tx_resp.value
            else:
                raise ValueError(f"Unsupported wallet client type: {type(agent.wallet_client).__name__}")

            if isinstance(signature, str):
                from solders.signature import Signature  # type: ignore
                signature = Signature.from_string(signature)

            await agent.connection.confirm_transaction(
                signature,
                commitment=Confirmed,
                last_valid_block_height=latest_blockhash.value.last_valid_block_height,
            )

            return str(signature)

        except Exception as e:
            raise Exception(f"Lending failed: {str(e)}")

    @staticmethod
    async def lulo_lend(agent: SolanaAgentKit, mint_address: str, amount: float) -> str:
        """
        Lend tokens for yields using Lulo.

        Args:
            agent (SolanaAgentKit): SolanaAgentKit instance.
            mint_address (str): SPL Mint address.
            amount (float): Amount to lend.

        Returns:
            str: Transaction signature.
        """
        try:
            url = f"{LuloManager.BASE_URL}/deposit?priorityFee=50000"
            headers = {
                "Content-Type": "application/json",
                "x-wallet-pubkey": str(agent.wallet_address if isinstance(agent.wallet_client, PrivyWalletClient) else agent.wallet.pubkey()),
                "x-api-key": agent.flexland_api_key
            }
            payload = json.dumps({
                "owner": str(agent.wallet_address if isinstance(agent.wallet_client, PrivyWalletClient) else agent.wallet.pubkey()),
                "mintAddress": mint_address,
                "depositAmount": str(amount)
            })

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    if response.status != 200:
                        raise Exception(f"Lulo API Error: {response.status}")
                    data = await response.json()

            transaction_bytes = base64.b64decode(data["data"]["transactionMeta"][0]["transaction"])
            lulo_txn = VersionedTransaction.from_bytes(transaction_bytes)

            latest_blockhash = await agent.connection.get_latest_blockhash()
            print("latest_blockhash", latest_blockhash)
            if isinstance(agent.wallet_client, PrivyWalletClient):
                res = await agent.wallet_client.send_transaction(data["data"]["transactionMeta"][0]["transaction"])
                print("res", res)
                tx_id = res.get("hash", "tx_id")
                print("tx_id", tx_id)
                signature = tx_id
            elif isinstance(agent.wallet_client, SolanaWalletClient):
                signature = agent.wallet.sign_message(to_bytes_versioned(lulo_txn.message))
                signed_tx = VersionedTransaction.populate(lulo_txn.message, [signature])
                tx_resp = await agent.connection.send_transaction(
                    signed_tx,
                    opts=TxOpts(preflight_commitment=Confirmed, max_retries=3)
                )
                tx_id = tx_resp.value
            else:
                raise ValueError(f"Unsupported wallet client type: {type(agent.wallet_client).__name__}")

            if isinstance(signature, str):
                from solders.signature import Signature  # type: ignore
                signature = Signature.from_string(signature)

            print("signature", signature)
            await agent.connection.confirm_transaction(
                signature,
                commitment=Confirmed,
                last_valid_block_height=latest_blockhash.value.last_valid_block_height,
            )

            return str(signature)

        except Exception as e:
            raise Exception(f"Lending failed: {str(e)}")

    @staticmethod
    async def lulo_withdraw(agent: SolanaAgentKit, mint_address: str, amount: float) -> str:
        """
        Withdraw tokens for yields using Lulo.

        Args:
            agent (SolanaAgentKit): SolanaAgentKit instance.
            mint_address (Pubkey): SPL Mint address.
            amount (float): Amount to withdraw.

        Returns:
            str: Transaction signature.
        """
        try:
            if not agent.flexland_api_key:
                raise Exception("Lulo API key not found in agent configuration")

            url = f"{LuloManager.BASE_URL}/withdraw?priorityFee=50000"
            headers = {
                "Content-Type": "application/json",
                "x-wallet-pubkey": str(agent.wallet_address if isinstance(agent.wallet_client, PrivyWalletClient) else agent.wallet.pubkey()),
                "x-api-key": agent.flexland_api_key
            }
            payload = json.dumps({
                "owner": str(agent.wallet_address if isinstance(agent.wallet_client, PrivyWalletClient) else agent.wallet.pubkey()),
                "mintAddress": mint_address,
                "depositAmount": str(amount)
            })

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    if response.status != 200:
                        raise Exception(f"Lulo API Error: {response.status}")
                    data = await response.json()

            transaction_bytes = base64.b64decode(data["data"]["transactionMeta"][0]["transaction"])
            lulo_txn = VersionedTransaction.from_bytes(transaction_bytes)

            latest_blockhash = await agent.connection.get_latest_blockhash()

            if isinstance(agent.wallet_client, PrivyWalletClient):
                res = await agent.wallet_client.send_transaction(data["data"]["transactionMeta"][0]["transaction"])
                tx_id = res.get("hash", "tx_id")
                signature = tx_id
            elif isinstance(agent.wallet_client, SolanaWalletClient):
                signature = agent.wallet.sign_message(to_bytes_versioned(lulo_txn.message))
                signed_tx = VersionedTransaction.populate(lulo_txn.message, [signature])
                tx_resp = await agent.connection.send_transaction(
                    signed_tx,
                    opts=TxOpts(preflight_commitment=Confirmed, max_retries=3)
                )
                tx_id = tx_resp.value
            else:
                raise ValueError(f"Unsupported wallet client type: {type(agent.wallet_client).__name__}")

            if isinstance(signature, str):
                from solders.signature import Signature  # type: ignore
                signature = Signature.from_string(signature)

            await agent.connection.confirm_transaction(
                signature,
                commitment=Confirmed,
                last_valid_block_height=latest_blockhash.value.last_valid_block_height,
            )

            return str(signature)

        except Exception as e:
            raise Exception(f"Withdraw failed: {str(e)}")
