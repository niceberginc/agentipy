import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class ElfaAiPingApiTool(BaseTool):
    name: str = "elfa_ai_ping_api"
    description: str = """
    Pings the Elfa AI API using ElfaAiManager.

    Input: None
    Output:
    {
        "api_response": "dict, the response from Elfa AI API",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str = None): 
        try:
            api_response = await self.agent_kit.ping_elfa_ai_api()
            return {
                "api_response": api_response,
                "message": "Success"
            }
        except Exception as e:
            return {
                "api_response": None,
                "message": f"Error pinging Elfa AI API: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


class ElfaAiGetApiKeyStatusTool(BaseTool):
    name: str = "elfa_ai_get_api_key_status"
    description: str = """
    Retrieves the status of the Elfa AI API key using ElfaAiManager.

    Input: None
    Output:
    {
        "api_key_status": "dict, the status of the API key",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str = None): 
        try:
            api_key_status = await self.agent_kit.get_elfa_ai_api_key_status()
            return {
                "api_key_status": api_key_status,
                "message": "Success"
            }
        except Exception as e:
            return {
                "api_key_status": None,
                "message": f"Error fetching Elfa AI API key status: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")