import base64

import requests
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
#from solana.transaction import Transaction
from solders.transaction import Transaction
from solders.keypair import Keypair  # type: ignore
from solders.pubkey import Pubkey as PublicKey  # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.types import GibworkCreateTaskResponse


class GibworkManager:
    @staticmethod        
    async def create_gibwork_task(
        agent: SolanaAgentKit,
        title: str,
        content: str,
        requirements: str,
        tags: list[str],
        token_mint_address: PublicKey,
        token_amount: int,
    ) -> GibworkCreateTaskResponse:
        try:
            payload = {
                "title": title,
                "content": content,
                "requirements": requirements,
                "tags": tags,
                "payer": str(agent.wallet_address),
                "token": {
                    "mintAddress": str(token_mint_address),
                    "amount": token_amount,
                },
            }

            response = requests.post(
                "https://api2.gib.work/tasks/public/transaction",
                headers={"Content-Type": "application/json"},
                json=payload,
            )
            response.raise_for_status()
            response_data = response.json()

            if not response_data.get("taskId") or not response_data.get("serializedTransaction"):
                raise Exception(response_data.get("message", "Unknown error occurred"))

            serialized_transaction = base64.b64decode(response_data["serializedTransaction"])
            transaction = Transaction.deserialize(serialized_transaction)
            transaction.sign(agent.wallet)

            signature = await agent.connection.send_transaction(
                transaction, agent.wallet, opts=TxOpts(skip_preflight=True)
            )

            latest_blockhash = await agent.connection.get_latest_blockhash()
            await agent.connection.confirm_transaction(
                {"signature": signature, "blockhash": latest_blockhash["blockhash"],
                "lastValidBlockHeight": latest_blockhash["lastValidBlockHeight"]}
            )

            return GibworkCreateTaskResponse(
                status="success",
                task_id=response_data["taskId"],
                signature=signature,
            )

        except Exception as err:
            raise Exception(f"Error creating task: {str(err)}")