from agentipy.agent import SolanaAgentKit
from agentipy.agent.evm import EvmAgentKit
import requests
import logging
import json
from typing import Union


logger = logging.getLogger(__name__)


class PythManager:
    @staticmethod
    async def get_price(
        agent: Union[SolanaAgentKit, EvmAgentKit], 
        base_token_ticker: str, 
        quote_token_ticker: str
    ):
        """
        Fetch price data for a given token mint address using the Pyth Oracle.
 
        :param agent: Agent kit (Solana or EVM)
        :param base_token_ticker: The ticker of the base token.
        :param quote_token_ticker: The ticker of the quote token.
        :return: A dictionary containing the price, ema_price, and raw_prices.
        """
        try: 
            payload = {
                "base_token_ticker": base_token_ticker,
                "quote_token_ticker": quote_token_ticker
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/pyth/getPrice",
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            response.raise_for_status()

            data = response.json()

            if data.get("success"):
                parsed_prices = json.loads(data.get("message"))
                return {
                    "success": True, 
                    "price": int(parsed_prices[0]['price']['price']) * (10 ** parsed_prices[0]['price']['expo']),
                    "ema_price": int(parsed_prices[0]['ema_price']['price']) * (10 ** parsed_prices[0]['ema_price']['expo']),
                    "raw_prices": parsed_prices[0]       
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(
                f"HTTP error during Pyth price retrieval: {http_error}", 
                exc_info=True
            )
            return {"success": False, "error": str(http_error)}
        
        except Exception as error:
            logger.error(
                f"Unexpected error during Pyth price retrieval: {error}", 
                exc_info=True
            )
            return {"success": False, "error": str(error)}