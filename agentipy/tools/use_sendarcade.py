import base64
import json

import aiohttp
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.message import to_bytes_versioned  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solders.transaction import VersionedTransaction  # type: ignore

from agentipy.agent import SolanaAgentKit


class SendArcadeManager:
    BASE_URL = "https://rps.sendarcade.fun"

    @staticmethod
    async def rock_paper_scissor(agent: SolanaAgentKit, amount: float, choice: str) -> str:
        """
        Play Rock Paper Scissors on the Sendarcade platform.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            amount (float): The amount of SOL to stake.
            choice (str): "rock", "paper", or "scissors".

        Returns:
            str: Game result message or transaction signature.
        """
        try:
            url = f"{SendArcadeManager.BASE_URL}/api/actions/bot?amount={amount}&choice={choice}"
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({"account": str(agent.wallet.pubkey())})

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    if response.status != 200:
                        raise Exception(f"RPS API Error: {response.status}")
                    data = await response.json()

            if "transaction" in data:
                transaction_bytes = base64.b64decode(data["transaction"])
                txn = VersionedTransaction.from_bytes(transaction_bytes)

                latest_blockhash = await agent.connection.get_latest_blockhash()
                txn.message.recent_blockhash = latest_blockhash.value.blockhash

                signature = agent.wallet.sign_message(to_bytes_versioned(txn.message))
                signed_tx = VersionedTransaction.populate(txn.message, [signature])

                tx_resp = await agent.connection.send_transaction(
                    signed_tx,
                    opts=TxOpts(preflight_commitment=Confirmed, max_retries=3)
                )
                tx_id = tx_resp.value

                await agent.connection.confirm_transaction(
                    tx_id,
                    commitment=Confirmed,
                    last_valid_block_height=latest_blockhash.value.last_valid_block_height,
                )

                next_href = data.get("links", {}).get("next", {}).get("href", "")
                return await SendArcadeManager.outcome(agent, str(signature), next_href) if next_href else "failed"
            else:
                return "failed"

        except Exception as e:
            raise Exception(f"RPS game failed: {str(e)}")

    @staticmethod
    async def outcome(agent: SolanaAgentKit, sig: str, href: str) -> str:
        """
        Retrieve the outcome of the Rock Paper Scissors game.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            sig (str): Transaction signature.
            href (str): API path for retrieving the outcome.

        Returns:
            str: Outcome message.
        """
        try:
            url = f"{SendArcadeManager.BASE_URL}{href}"
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({"account": str(agent.wallet.pubkey()), "signature": sig})

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    if response.status != 200:
                        raise Exception(f"RPS outcome API Error: {response.status}")
                    data = await response.json()

            title = data.get("title", "")
            if title.startswith("You lost"):
                return title

            next_href = data.get("links", {}).get("actions", [{}])[0].get("href", "")
            return f"{title}\n{await SendArcadeManager.won(agent, next_href)}" if next_href else title

        except Exception as e:
            raise Exception(f"RPS outcome failed: {str(e)}")

    @staticmethod
    async def won(agent: SolanaAgentKit, href: str) -> str:
        """
        Handle the winner transaction process.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            href (str): API path for claiming the prize.

        Returns:
            str: Success message or failure notice.
        """
        try:
            url = f"{SendArcadeManager.BASE_URL}{href}"
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({"account": str(agent.wallet.pubkey())})

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    if response.status != 200:
                        raise Exception(f"RPS claim API Error: {response.status}")
                    data = await response.json()

            if "transaction" in data:
                transaction_bytes = base64.b64decode(data["transaction"])
                txn = VersionedTransaction.from_bytes(transaction_bytes)

                signature = agent.wallet.sign_message(to_bytes_versioned(txn.message))
                signed_tx = VersionedTransaction.populate(txn.message, [signature])

                await agent.connection.send_transaction(
                    signed_tx,
                    opts=TxOpts(preflight_commitment=Confirmed)
                )
            else:
                return "Failed to claim prize."

            next_href = data.get("links", {}).get("next", {}).get("href", "")
            return await SendArcadeManager.post_win(agent, next_href) if next_href else "Prize claim completed."

        except Exception as e:
            raise Exception(f"RPS claim failed: {str(e)}")

    @staticmethod
    async def post_win(agent: SolanaAgentKit, href: str) -> str:
        """
        Complete the prize claim process.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.
            href (str): API path for finalizing the prize claim.

        Returns:
            str: Confirmation message.
        """
        try:
            url = f"{SendArcadeManager.BASE_URL}{href}"
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({"account": str(agent.wallet.pubkey())})

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as response:
                    if response.status != 200:
                        raise Exception(f"RPS finalization API Error: {response.status}")
                    data = await response.json()

            title = data.get("title", "Unknown result")
            return f"Prize claimed Successfully\n{title}"

        except Exception as e:
            raise Exception(f"RPS outcome failed: {str(e)}")
