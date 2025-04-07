import asyncio
import struct

import base58
import spl.token.instructions as spl_token
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
#from solana.transaction import Transaction
from solders.transaction import Transaction
from solders.instruction import AccountMeta, Instruction  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from spl.token.instructions import get_associated_token_address

from agentipy.agent import SolanaAgentKit
from agentipy.constants import (EXPECTED_DISCRIMINATOR, LAMPORTS_PER_SOL,
                                PUMP_EVENT_AUTHORITY, PUMP_FEE, PUMP_GLOBAL,
                                PUMP_PROGRAM,
                                SYSTEM_ASSOCIATED_TOKEN_ACCOUNT_PROGRAM,
                                SYSTEM_PROGRAM, SYSTEM_RENT,
                                SYSTEM_TOKEN_PROGRAM, TOKEN_DECIMALS)
from agentipy.types import BondingCurveState


class PumpfunManager:
    @staticmethod
    async def get_pump_curve_state(conn: AsyncClient, curve_address: Pubkey) -> BondingCurveState:
        response = await conn.get_account_info(curve_address)
        if not response.value or not response.value.data:
            raise ValueError("Invalid curve state: No data")

        data = response.value.data
        if data[:8] != EXPECTED_DISCRIMINATOR:
            raise ValueError("Invalid curve state discriminator")

        return BondingCurveState(data)

    @staticmethod
    def calculate_pump_curve_price(curve_state: BondingCurveState) -> float:
        if curve_state.virtual_token_reserves <= 0 or curve_state.virtual_sol_reserves <= 0:
            raise ValueError("Invalid reserve state")
        return (curve_state.virtual_sol_reserves / LAMPORTS_PER_SOL) / (curve_state.virtual_token_reserves / 10 ** TOKEN_DECIMALS)
    
    @staticmethod
    async def get_token_balance(conn: AsyncClient, associated_token_account: Pubkey):
        response = await conn.get_token_account_balance(associated_token_account)
        if response.value:
            return int(response.value.amount)
        return 0

    @staticmethod
    async def buy_token(agent: SolanaAgentKit, mint: Pubkey, bonding_curve: Pubkey, associated_bonding_curve: Pubkey, amount: float, slippage: float = 0.01, max_retries=5):
        payer = agent.wallet

        async with AsyncClient(agent.rpc_url) as client:
            associated_token_account = get_associated_token_address(payer.pubkey(), mint)
            amount_lamports = int(amount * LAMPORTS_PER_SOL)

            # Fetch the token price
            curve_state = await PumpfunManager.get_pump_curve_state(client, bonding_curve)
            token_price_sol = PumpfunManager.calculate_pump_curve_price(curve_state)
            token_amount = amount / token_price_sol

            # Calculate maximum SOL to spend with slippage
            max_amount_lamports = int(amount_lamports * (1 + slippage))

            # Create associated token account with retries
            for ata_attempt in range(max_retries):
                try:
                    account_info = await client.get_account_info(associated_token_account)
                    if account_info.value is None:
                        print(f"Creating associated token account (Attempt {ata_attempt + 1})...")
                        create_ata_ix = spl_token.create_associated_token_account(
                            payer=payer.pubkey(),
                            owner=payer.pubkey(),
                            mint=mint
                        )
                        create_ata_tx = Transaction()
                        create_ata_tx.add(create_ata_ix)
                        recent_blockhash = await client.get_latest_blockhash()
                        create_ata_tx.recent_blockhash = recent_blockhash.value.blockhash
                        await client.send_transaction(create_ata_tx, payer)
                        print("Associated token account created.")
                        print(f"Associated token account address: {associated_token_account}")
                        break
                    else:
                        print("Associated token account already exists.")
                        print(f"Associated token account address: {associated_token_account}")
                        break
                except Exception as e:
                    print(f"Attempt {ata_attempt + 1} to create associated token account failed: {str(e)}")
                    if ata_attempt < max_retries - 1:
                        wait_time = 2 ** ata_attempt
                        print(f"Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        print("Max retries reached. Unable to create associated token account.")
                        return

            # Continue with the buy transaction
            for attempt in range(max_retries):
                try:
                    accounts = [
                        AccountMeta(pubkey=PUMP_GLOBAL, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=PUMP_FEE, is_signer=False, is_writable=True),
                        AccountMeta(pubkey=mint, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=bonding_curve, is_signer=False, is_writable=True),
                        AccountMeta(pubkey=associated_bonding_curve, is_signer=False, is_writable=True),
                        AccountMeta(pubkey=associated_token_account, is_signer=False, is_writable=True),
                        AccountMeta(pubkey=payer.pubkey(), is_signer=True, is_writable=True),
                        AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=SYSTEM_TOKEN_PROGRAM, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=SYSTEM_RENT, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=PUMP_EVENT_AUTHORITY, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=PUMP_PROGRAM, is_signer=False, is_writable=False),
                    ]

                    discriminator = struct.pack("<Q", 16927863322537952870)
                    data = discriminator + struct.pack("<Q", int(token_amount * 10**6)) + struct.pack("<Q", max_amount_lamports)
                    buy_ix = Instruction(PUMP_PROGRAM, data, accounts)

                    recent_blockhash = await client.get_latest_blockhash()
                    transaction = Transaction()
                    transaction.add(buy_ix)
                    transaction.recent_blockhash = recent_blockhash.value.blockhash

                    tx = await client.send_transaction(
                        transaction,
                        payer,
                        opts=TxOpts(skip_preflight=True, preflight_commitment=Confirmed),
                    )

                    print(f"Transaction sent: https://explorer.solana.com/tx/{tx.value}")

                    await client.confirm_transaction(tx.value, commitment="confirmed")
                    print("Transaction confirmed")
                    return tx.value

                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        print(f"Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        print("Max retries reached. Unable to complete the transaction.")

    @staticmethod
    async def sell_token(agent: SolanaAgentKit, mint: Pubkey, bonding_curve: Pubkey, associated_bonding_curve: Pubkey, slippage: float = 0.25, max_retries=5):
        payer = agent.wallet

        async with AsyncClient(agent.rpc_url) as client:
            associated_token_account = get_associated_token_address(payer.pubkey(), mint)
            
            # Get token balance
            token_balance = await PumpfunManager.get_token_balance(client, associated_token_account)
            token_balance_decimal = token_balance / 10**TOKEN_DECIMALS
            print(f"Token balance: {token_balance_decimal}")
            if token_balance == 0:
                print("No tokens to sell.")
                return

            # Fetch the token price
            curve_state = await PumpfunManager.get_pump_curve_state(client, bonding_curve)
            token_price_sol = PumpfunManager.calculate_pump_curve_price(curve_state)
            print(f"Price per Token: {token_price_sol:.20f} SOL")

            # Calculate minimum SOL output
            amount = token_balance
            min_sol_output = float(token_balance_decimal) * float(token_price_sol)
            slippage_factor = 1 - slippage
            min_sol_output = int((min_sol_output * slippage_factor) * LAMPORTS_PER_SOL)
            
            print(f"Selling {token_balance_decimal} tokens")
            print(f"Minimum SOL output: {min_sol_output / LAMPORTS_PER_SOL:.10f} SOL")

            for attempt in range(max_retries):
                try:
                    accounts = [
                        AccountMeta(pubkey=PUMP_GLOBAL, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=PUMP_FEE, is_signer=False, is_writable=True),
                        AccountMeta(pubkey=mint, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=bonding_curve, is_signer=False, is_writable=True),
                        AccountMeta(pubkey=associated_bonding_curve, is_signer=False, is_writable=True),
                        AccountMeta(pubkey=associated_token_account, is_signer=False, is_writable=True),
                        AccountMeta(pubkey=payer.pubkey(), is_signer=True, is_writable=True),
                        AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=SYSTEM_ASSOCIATED_TOKEN_ACCOUNT_PROGRAM, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=SYSTEM_TOKEN_PROGRAM, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=PUMP_EVENT_AUTHORITY, is_signer=False, is_writable=False),
                        AccountMeta(pubkey=PUMP_PROGRAM, is_signer=False, is_writable=False),
                    ]

                    discriminator = struct.pack("<Q", 12502976635542562355)
                    data = discriminator + struct.pack("<Q", amount) + struct.pack("<Q", min_sol_output)
                    sell_ix = Instruction(PUMP_PROGRAM, data, accounts)

                    recent_blockhash = await client.get_latest_blockhash()
                    transaction = Transaction()
                    transaction.add(sell_ix)
                    transaction.recent_blockhash = recent_blockhash.value.blockhash

                    tx = await client.send_transaction(
                        transaction,
                        payer,
                        opts=TxOpts(skip_preflight=True, preflight_commitment=Confirmed),
                    )

                    print(f"Transaction sent: https://explorer.solana.com/tx/{tx.value}")

                    await client.confirm_transaction(tx.value, commitment="confirmed")
                    print("Transaction confirmed")

                    return tx.value

                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        print(f"Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        print("Max retries reached. Unable to complete the transaction.")
