import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class AlloraGetInferenceByTopicIdTool(BaseTool):
    name: str = "allora_get_inference_by_topic_id"
    description: str = """
    Fetches a price inference for BTC or ETH for a given timeframe (5m or 8h) from the Allora Network using AlloraManager.

    Input: A JSON string with:
    {
        "topic_id": "int, the topic ID to fetch inference for"
    }
    Output:
    {
        "inference_data": "dict, the inferred price and confidence interval",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "topic_id": {"type": int, "required": True}
            }
            validate_input(data, schema)
            inference_data = await self.agent_kit.get_inference_by_topic_id(
                topic_id=data["topic_id"]
            )
            return {
                "inference_data": inference_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "inference_data": None,
                "message": f"Error fetching price inference: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")