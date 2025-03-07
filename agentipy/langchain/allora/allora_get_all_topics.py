from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
class AlloraGetAllTopicsTool(BaseTool):
    name: str = "allora_get_all_topics"
    description: str = """
    Fetches all topics from the Allora Network using AlloraManager.

    Input: None
    Output:
    {
        "topics": "list, the list of topic IDs",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self):
        try:
            topics = await self.agent_kit.get_all_topics()
            return {
                "topics": topics,
                "message": "Success"
            }
        except Exception as e:
            return {
                "topics": None,
                "message": f"Error fetching all topics: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")