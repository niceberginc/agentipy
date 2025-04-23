import asyncio
import logging
from pythclient.pythaccounts import PythPriceAccount, PythPriceStatus
from pythclient.solana import SolanaClient, SolanaPublicKey, PYTHNET_HTTP_ENDPOINT, PYTHNET_WS_ENDPOINT

logger = logging.getLogger(__name__)

class PythManager:
    @staticmethod
    async def get_price(mint_address: str) -> dict:
        """
        Fetch price data for a given Pyth feed mint address using the official pythclient.

        :param mint_address: The Pyth price account public key.
        :return: A dict with keys: 'status', 'price', 'confidence_interval' (if trading).
        """
        client = SolanaClient(endpoint=PYTHNET_HTTP_ENDPOINT, ws_endpoint=PYTHNET_WS_ENDPOINT)
        try:
            price_account = PythPriceAccount(SolanaPublicKey(mint_address), client)
            await price_account.update()
            status = price_account.aggregate_price_status
            response = {"status": status.name}
            if status == PythPriceStatus.TRADING:
                response.update({
                    "price": price_account.aggregate_price,
                    "confidence_interval": price_account.aggregate_price_confidence_interval
                })
            return response
        except Exception as e:
            logger.error(f"Error fetching Pyth price for {mint_address}: {e}", exc_info=True)
            return {"status": "ERROR", "message": str(e)}
        finally:
            await client.close()

async def get_prices(
    feeds: dict[str, str]
) -> dict[str, dict]:
    """
    Fetch multiple Pyth feeds concurrently using PythManager.

    :param feeds: Mapping from symbol (e.g. "SOL/USD") to mint_address.
    :return: Mapping from symbol to the result dict from get_price().
    """
    results: dict[str, dict] = {}
    tasks: dict[str, asyncio.Task] = {
        symbol: asyncio.create_task(PythManager.get_price(addr))
        for symbol, addr in feeds.items()
    }
    for symbol, task in tasks.items():
        results[symbol] = await task
    return results
