import json

from allora_sdk.v2.api_client import (PriceInferenceTimeframe,
                                      PriceInferenceToken, SignatureFormat)
from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class AlloraGetPricePredictionTool(BaseTool):
    name: str = "allora_get_price_prediction"
    description: str = """
    Fetches a future price prediction for BTC or ETH for a given timeframe (5m or 8h) from the Allora Network using AlloraManager.

    Input: A JSON string with:
    {
        "asset": "string, the crypto asset symbol (e.g., 'BTC' or 'ETH')",
        "timeframe": "string, the prediction timeframe ('5m' or '8h')",
        "signature_format": "string, optional, the signature format (default: 'ETHEREUM_SEPOLIA')"
    }
    Output:
    {
        "price_prediction": "dict, the predicted price and confidence interval",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "asset": {"type": str, "required": True},
                "timeframe": {"type": str, "required": True},
                "signature_format": {"type": str, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)
            price_prediction = await self.agent_kit.get_price_prediction(
                asset=PriceInferenceToken[data["asset"]],
                timeframe=PriceInferenceTimeframe[data["timeframe"]],
                signature_format=SignatureFormat[data.get("signature_format", "ETHEREUM_SEPOLIA")]
            )
            return {
                "price_prediction": price_prediction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "price_prediction": None,
                "message": f"Error fetching price prediction: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
