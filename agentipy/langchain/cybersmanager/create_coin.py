import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaCybersCreateCoinTool(BaseTool):
    name: str = "cybers_create_coin"
    description: str = """
    Creates a new coin using the CybersManager.

    Input: A JSON string with:
    {
        "name": "string, the name of the coin",
        "symbol": "string, the symbol of the coin",
        "image_path": "string, the file path to the coin's image",
        "tweet_author_id": "string, the Twitter ID of the coin's author",
        "tweet_author_username": "string, the Twitter username of the coin's author"
    }

    Output:
    {
        "coin_id": "string, the unique ID of the created coin",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "name": {"type": str, "required": True},
                "symbol": {"type": str, "required": True},
                "image_path": {"type": str, "required": True},
                "tweet_author_id": {"type": str, "required": True},
                "tweet_author_username": {"type": str, "required": True}
            }
            validate_input(data, schema)

            name = data["name"]
            symbol = data["symbol"]
            image_path = data["image_path"]
            tweet_author_id = data["tweet_author_id"]
            tweet_author_username = data["tweet_author_username"]

            coin_id = await self.solana_kit.cybers_create_coin(
                name=name,
                symbol=symbol,
                image_path=image_path,
                tweet_author_id=tweet_author_id,
                tweet_author_username=tweet_author_username
            )
            return {
                "coin_id": coin_id,
                "message": "Success"
            }
        except Exception as e:
            return {
                "coin_id": None,
                "message": f"Error creating coin: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

