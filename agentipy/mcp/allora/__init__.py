from allora_sdk.v2.api_client import (PriceInferenceTimeframe,
                                      PriceInferenceToken, SignatureFormat)

from agentipy.mcp.type import ActionType
from agentipy.tools.use_allora import AlloraManager

ALLORA_ACTIONS = {
    "GET_ALL_TOPICS": ActionType(
        name="GET_ALL_TOPICS",
        description="Get all topics from Allora's API",
        schema={},
        handler=lambda agent, params: AlloraManager.get_all_topics(agent),
    ),
     "GET_PRICE_PREDICTION": ActionType(
        name="GET_PRICE_PREDICTION",
        description="Fetch a future price prediction for BTC or ETH for a given timeframe from the Allora Network.",
        schema={
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
        handler=lambda agent, params: agent.get_price_prediction(
            asset=PriceInferenceToken[params["asset"]],
            timeframe=PriceInferenceTimeframe[params["timeframe"]],
            signature_format=SignatureFormat[params.get("signature_format", "ETHEREUM_SEPOLIA")],
        ),
    ),
    
    "GET_INFERENCE_BY_TOPIC_ID": ActionType(
        name="GET_INFERENCE_BY_TOPIC_ID",
        description="Fetch inference data for a specific topic ID.",
        schema={
            "topic_id": {"type": "integer", "description": "Topic ID to fetch inference data for."},
        },
        handler=lambda agent, params: agent.get_inference_by_topic_id(params["topic_id"]),
    ),
}
