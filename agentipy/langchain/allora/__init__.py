from agentipy.langchain.allora.allora_get_all_topics import AlloraGetAllTopicsTool
from agentipy.langchain.allora.allora_get_inference_by_topic_id import AlloraGetInferenceByTopicIdTool
from agentipy.langchain.allora.allora_get_price_prediction import AlloraGetPricePredictionTool
from agentipy.agent import SolanaAgentKit

def  get_allora_tools(agent_kit: SolanaAgentKit):
    return [
        AlloraGetAllTopicsTool(agent_kit=agent_kit),
        AlloraGetInferenceByTopicIdTool(agent_kit=agent_kit),
        AlloraGetPricePredictionTool(agent_kit=agent_kit)
    ]