import logging
from typing import Optional

import aiohttp
from solders.pubkey import Pubkey  # type: ignore

from agentipy.types import JupiterTokenData

logger = logging.getLogger(__name__)

class TokenDataManager:
    @staticmethod
    async def get_token_data_by_address(mint: str) -> Optional[JupiterTokenData]:
        try:
            if not mint:
                raise ValueError("Mint address is required")

            async with aiohttp.ClientSession() as session:
                async with session.get("https://tokens.jup.ag/tokens?tags=verified", headers={"Content-Type": "application/json"}) as response:
                    response.raise_for_status()
                    data = await response.json()
                    for token in data:
                        if token.get("address") == mint:
                            return JupiterTokenData(
                                address=token.get("address"),
                                symbol=token.get("symbol"),
                                name=token.get("name"),
                            )
                    return None
        except Exception as error:
            raise Exception(f"Error fetching token data: {str(error)}")
        
    @staticmethod
    async def get_token_address_from_ticker(ticker: str) -> Optional[str]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.dexscreener.com/latest/dex/search?q={ticker}") as response:
                    response.raise_for_status()
                    data = await response.json()
                    if not data.get("pairs"):
                        return None

                    solana_pairs = [
                        pair for pair in data["pairs"] if pair.get("chainId") == "solana"
                    ]
                    solana_pairs.sort(key=lambda x: x.get("fdv", 0), reverse=True)

                    solana_pairs = [
                        pair
                        for pair in solana_pairs
                        if pair.get("baseToken", {}).get("symbol", "").lower() == ticker.lower()
                    ]

                    if solana_pairs:
                        return solana_pairs[0].get("baseToken", {}).get("address")
                    return None
        except Exception as error:
            logger.error(f"Error fetching token address from DexScreener: {str(error)}", exc_info=True)
            return None
        
    @staticmethod
    async def get_token_data_by_ticker(ticker: str) -> Optional[JupiterTokenData]:
        address = await TokenDataManager.get_token_address_from_ticker(ticker)
        if not address:
            raise ValueError(f"Token address not found for ticker: {ticker}")
        
        return await TokenDataManager.get_token_data_by_address(address)
