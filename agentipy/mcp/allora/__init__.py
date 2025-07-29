from allora_sdk.v2.api_client import (PriceInferenceTimeframe,
                                      PriceInferenceToken, SignatureFormat)
from mcp.types import Tool

from agentipy.tools.use_allora import AlloraManager

ALLORA_ACTIONS = {
    "GET_ALL_TOPICS": Tool(
        name="GET_ALL_TOPICS",
        description="Get all topics from Allora's API. input_schema Example: {}",
        inputSchema={},
        handler=lambda agent, params: AlloraManager(agent).get_all_topics(),
    ),

    "GET_PRICE_PREDICTION": Tool(
        name="GET_PRICE_PREDICTION",
        description=(
            "Fetch a future price prediction for BTC or ETH for a given timeframe from the Allora Network. "
            "input_schema Example: { asset: string, timeframe: string, signature_format: string = 'ETHEREUM_SEPOLIA' }"
        ),
        inputSchema={
            "asset": {
                "type": "string",
                "description": "Crypto asset symbol (BTC or ETH).",
                "enum": ["BTC", "ETH"],
            },
            "timeframe": {
                "type": "string",
                "description": "Prediction timeframe (FIVE_MINUTES or EIGHT_HOURS).",
                "enum": ["FIVE_MINUTES", "EIGHT_HOURS"],
            },
            "signature_format": {
                "type": "string",
                "description": "Blockchain signature format (default: ETHEREUM_SEPOLIA).",
                "enum": ["ETHEREUM_SEPOLIA", "ETHEREUM_MAINNET"],
                "default": "ETHEREUM_SEPOLIA",
            },
        },
        handler=lambda agent, params: AlloraManager(agent).get_price_prediction(
            asset=PriceInferenceToken[params["asset"]],
            timeframe=PriceInferenceTimeframe[params["timeframe"]],
            signature_format=SignatureFormat[params.get("signature_format", "ETHEREUM_SEPOLIA")],
        ),
    ),

    "GET_INFERENCE_BY_TOPIC_ID": Tool(
        name="GET_INFERENCE_BY_TOPIC_ID",
        description="Fetch inference data for a specific topic ID. input_schema Example: { topic_id: number }",
        inputSchema={
            "topic_id": {
                "type": "integer",
                "description": "Topic ID to fetch inference data for."
            },
        },
        handler=lambda agent, params: AlloraManager(agent).get_inference_by_topic_id(params["topic_id"]),
    ),
}
