from agentipy.agent import SolanaAgentKit
from agentipy.utils.stork.utils import get_stork_price


class StorkManager:
    @staticmethod
    async def get_price(agent: SolanaAgentKit, asset_id: str):
        """
        Fetch price data for a given asset using the Stork Oracle.

        :param agent: SolanaAgentKit instance with a Stork API key.
        :param asset_id: The plaintext asset ID to fetch price data for.
        :return: A dictionary containing the price and timestamp. 
        """
        price = get_stork_price(asset_id.upper(), agent.stork_api_key)
        
        if "error" in price:
            raise Exception(price["error"])
        
        if "data" not in price:
            raise Exception("No data found in price response")

        price_data = price["data"][asset_id.upper()]
        price = price_data["price"]

        # convert price to float, divide by 10^18
        price = float(price) / 10**18
        timestamp = price_data["timestamp"]

        result = {
            "price": price,
            "timestamp": timestamp
        }

        return result

