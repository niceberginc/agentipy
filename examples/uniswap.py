
import asyncio
from agentipy.agent.evm import EvmAgentKit
from agentipy.utils.evm.general.decimal_converter import from_readable_amount
from agentipy.utils.evm.general.networks import BaseRPC
from agentipy.utils.evm.tokens.base import USDC_BASE, WETH_BASE


async def main():
    """
    Quick Start Example: Get Quote and Trade with Uniswap on Base.
    """
    # **!!! IMPORTANT SECURITY WARNING !!!**
    # NEVER hardcode your private key directly into your code, ESPECIALLY for Mainnet.
    # This is for demonstration purposes ONLY.
    # In a real application, use environment variables, secure key vaults, or other
    # secure key management practices.  Compromising your private key can lead to
    # loss of funds.

    PRIVATE_KEY = ""  # ⚠️ REPLACE THIS SECURELY! ⚠️

    agent = EvmAgentKit(
        network=BaseRPC,
        private_key=PRIVATE_KEY,
    )
 
    try:
        # If desired token data is not in the agent's token list, 
        # you can manually enter the addresses (str) and decimals (int)
        getQuote = await agent.get_uniswap_quote(
            input_token_address=WETH_BASE.address, 
            output_token_address=USDC_BASE.address,  
            amount_in_raw="5000000000000",  
            input_token_decimals=WETH_BASE.decimals,  
            output_token_decimals=USDC_BASE.decimals, 
            slippage=0.5, 
        )

        getQuoteFromReadable = await agent.get_uniswap_quote(
            input_token_address=WETH_BASE.address, 
            output_token_address=USDC_BASE.address,  
            amount_in_raw=from_readable_amount(0.000005, WETH_BASE.decimals), # Input amount in readable format
            input_token_decimals=WETH_BASE.decimals,  
            output_token_decimals=USDC_BASE.decimals,  
            slippage=0.5,  
        )

        print(getQuote["message"])
        print(getQuoteFromReadable["message"])

        trade = await agent.trade_on_uniswap(
            input_token_address=WETH_BASE.address, 
            output_token_address=USDC_BASE.address,
            amount_in_raw="5000000000000", 
            input_token_decimals=WETH_BASE.decimals, 
            output_token_decimals=USDC_BASE.decimals, 
            slippage=0.5, 
        )

        print(trade)

    except RuntimeError as e:
        print(f"Error: Transfer failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())