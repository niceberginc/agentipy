import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SwitchboardSimulateFeedTool(BaseTool):
    name: str = "switchboard_simulate_feed"
    description: str = """
    Simulate a Switchboard feed.

    Input: A JSON string with:
    {
        "feed": "string, the name of the Switchboard feed to simulate.",
        "crossbar_url": "string, optional, the Crossbar URL for additional configuration."
    }

    Output:
    {
        "simulation_details": "dict, the details of the simulation",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "feed": {"type": str, "required": True},
                "crossbar_url": {"type": str, "required": False},
            }
            validate_input(data, schema)

            feed = data["feed"]
            crossbar_url = data.get("crossbar_url")

            result = await self.solana_kit.simulate_switchboard_feed(feed, crossbar_url)
            return {
                "status": "success",
                "simulation_details": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
