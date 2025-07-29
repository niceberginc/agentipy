import base64
import logging
from typing import Union

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solana.transaction import Transaction  # type: ignore
from solders.message import Message  # type: ignore
from solders.null_signer import NullSigner  # type: ignore
from solders.pubkey import Pubkey as PublicKey  # type: ignore
from solders.system_program import TransferParams, transfer
from spl.token.async_client import AsyncToken
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import (get_associated_token_address,
                                    transfer_checked)
from web3 import Web3

from agentipy.agent import SolanaAgentKit
from agentipy.agent.evm import EvmAgentKit
from agentipy.wallet.evm_wallet_client import EVMTransaction
from agentipy.wallet.privy_wallet_client import PrivyWalletClient
from agentipy.wallet.solana_wallet_client import (SolanaTransaction,
                                                  SolanaWalletClient)

LAMPORTS_PER_SOL = 10**9

logger = logging.getLogger(__name__)


class TokenTransferManager:
    @staticmethod
    async def transfer_evm(
        agent: EvmAgentKit, to: str, amount: float, token_address: str = None
    ) -> str:
        """
        Transfer native EVM currency or ERC20 tokens to a recipient using Privy.
        """
        try:
            amount_in_wei = Web3.to_wei(amount, "ether")

            if token_address:
                # TODO: Implement ERC20 transfer logic
                # This would involve constructing the transaction data for the 'transfer' function
                # of the ERC20 contract.
                raise NotImplementedError(
                    "ERC20 token transfers are not yet implemented."
                )
            else:
                # Native currency transfer
                evm_tx = EVMTransaction(
                    to=to,
                    value=amount_in_wei,
                    data="0x",  # No data for native transfer
                    gas=None,  # Let Privy handle gas estimation
                )

            if not isinstance(agent.wallet_client, PrivyWalletClient):
                raise ValueError(
                    f"Unsupported wallet client type for EVM transfer: {type(agent.wallet_client).__name__}"
                )

            res = await agent.wallet_client.send_transaction(evm_tx)
            tx_hash = res.get("hash")

            if not tx_hash:
                raise RuntimeError("Transaction failed, no hash returned.")

            logging.info(f"EVM Transaction Hash: {tx_hash}")
            return str(tx_hash)

        except Exception as e:
            raise RuntimeError(f"EVM Transfer failed: {str(e)}")

    @staticmethod
    async def transfer(
        agent: Union[SolanaAgentKit, EvmAgentKit],
        to: str,
        amount: float,
        mint_or_token_address: str = None,
    ) -> str:
        """
        Transfer tokens or native currency based on the agent type.
        For SolanaAgentKit: Transfers SOL or SPL tokens. `mint_or_token_address` is the mint address for SPL tokens.
        For EvmAgentKit: Transfers native EVM currency or ERC20 tokens. `mint_or_token_address` is the token contract address for ERC20.
        """
        if isinstance(agent, EvmAgentKit):
            # Handle EVM transfer
            return await TokenTransferManager.transfer_evm(
                agent, to, amount, token_address=mint_or_token_address
            )
        elif isinstance(agent, SolanaAgentKit):
            # Handle Solana transfer (existing logic)
            try:
                print(
                    f"Transferring {amount} {'SPL' if mint_or_token_address else 'SOL'} to {to} from {agent.wallet_address}"
                )
                to_pubkey = PublicKey.from_string(to)
                from_pubkey = PublicKey.from_string(str(agent.wallet_address))

                blockhash_resp = await agent.connection.get_latest_blockhash()
                recent_blockhash = blockhash_resp.value.blockhash

                instructions = []

                if mint_or_token_address is None:
                    # SOL Transfer
                    instructions.append(
                        transfer(
                            TransferParams(
                                from_pubkey=from_pubkey,
                                to_pubkey=to_pubkey,
                                lamports=int(amount * LAMPORTS_PER_SOL),
                            )
                        )
                    )
                else:
                    # SPL Token Transfer
                    mint_pubkey = PublicKey.from_string(mint_or_token_address)

                    async with AsyncClient(agent.rpc_url) as client:
                        token = AsyncToken(
                            client, mint_pubkey, TOKEN_PROGRAM_ID, NullSigner()
                        )  # Added NullSigner

                        from_ata = get_associated_token_address(
                            from_pubkey, mint_pubkey
                        )  # Use sync version
                        to_ata = get_associated_token_address(
                            to_pubkey, mint_pubkey
                        )  # Use sync version

                        resp = await client.get_account_info(to_ata)
                        if resp.value is None:
                            from spl.token.instructions import \
                                create_associated_token_account

                            ata_ix = create_associated_token_account(
                                from_pubkey, to_pubkey, mint_pubkey
                            )
                            instructions.append(ata_ix)

                        mint_info = await token.get_mint_info()
                        adjusted_amount = int(amount * (10**mint_info.decimals))

                        instructions.append(
                            transfer_checked(
                                source=from_ata,
                                dest=to_ata,
                                owner=from_pubkey,
                                amount=adjusted_amount,
                                decimals=mint_info.decimals,
                                mint=mint_pubkey,
                                program_id=TOKEN_PROGRAM_ID,
                            )
                        )

                # Detect Wallet Client Type for Solana
                if isinstance(agent.wallet_client, PrivyWalletClient):
                    transaction = Transaction()
                    for instruction in instructions:
                        transaction.add(instruction)
                    transaction.recent_blockhash = recent_blockhash
                    transaction.fee_payer = from_pubkey  # Set fee payer
                    serialized_transaction = transaction.serialize(
                        verify_signatures=False
                    )
                    transaction_base64 = base64.b64encode(
                        serialized_transaction
                    ).decode("utf-8")
                    res = await agent.wallet_client.send_transaction(transaction_base64)
                    tx_id = res.get("hash")  # Privy returns 'hash'
                elif isinstance(agent.wallet_client, SolanaWalletClient):
                    solana_tx = SolanaTransaction(
                        instructions=instructions,
                    )  # Pass blockhash and fee payer
                    
                    res = await agent.wallet_client.send_transaction(solana_tx)
                    logger.info(f"Transaction response: {res}")
                    tx_id = res.get("hash") 
                else:
                    # Fallback for other wallet types
                    raise ValueError(
                        f"Unsupported wallet client type for Solana: {type(agent.wallet_client).__name__}"
                    )

                if not tx_id:
                    raise RuntimeError(
                        "Transaction failed, no signature/hash returned."
                    )

                logging.info(f"Solana Transaction Signature/Hash: {tx_id}")
                return str(tx_id)

            except Exception as e:
                raise RuntimeError(f"Solana Transfer failed: {str(e)}")
        else:
            raise TypeError(
                f"Unsupported agent type: {type(agent).__name__}. Must be SolanaAgentKit or EvmAgentKit."
            )
