from solana.rpc.async_api import AsyncClient
#from solana.transaction import Transaction
from solders.transaction import Transaction
from solders.pubkey import Pubkey as PublicKey  # type: ignore
from solders.system_program import TransferParams, transfer
from spl.token.async_client import AsyncToken

from agentipy.agent import SolanaAgentKit

LAMPORTS_PER_SOL = 10**9

class TokenTransferManager:
    @staticmethod

    async def transfer(agent:SolanaAgentKit, to: str, amount: float, mint: str = None) -> str:
        """
        Transfer SOL or SPL tokens to a recipient.

        :param agent: An instance of SolanaAgentKit
        :param to: Recipient's public key
        :param amount: Amount to transfer
        :param mint: Optional mint address for SPL tokens
        :return: Transaction signature
        """
        try:
            # Convert to PublicKey objects
            to_pubkey = PublicKey.from_string(to)
            wallet_pubkey = agent.wallet_address

            if mint is None:
                # Transfer native SOL
                transaction = Transaction()
                transaction.add(
                    transfer(
                        TransferParams(
                            from_pubkey=wallet_pubkey,
                            to_pubkey=to_pubkey,
                            lamports=int(amount * LAMPORTS_PER_SOL),
                        )
                    )
                )
            else:
                mint_pubkey = PublicKey.from_string(mint)
                async with AsyncClient(agent.rpc_url) as client:
                    token = AsyncToken(client, mint_pubkey)
                    
                    from_ata = await token.get_associated_token_address(wallet_pubkey)
                    to_ata = await token.get_associated_token_address(to_pubkey)

                    mint_info = await token.get_mint_info()
                    adjusted_amount = int(amount * (10**mint_info.decimals))

                    transaction = Transaction()
                    transaction.add(
                        token.transfer_checked(
                            from_ata,
                            to_ata,
                            wallet_pubkey,
                            adjusted_amount,
                            mint_info.decimals,
                        )
                    )
            blockhash_response = await agent.connection.get_latest_blockhash()
            recent_blockhash = blockhash_response.value.blockhash
            transaction.recent_blockhash = recent_blockhash
            transaction.sign(agent.wallet)

            signature = await agent.connection.send_raw_transaction(transaction.serialize())
            return signature
        except Exception as e:
            raise RuntimeError(f"Transfer failed: {str(e)}")
