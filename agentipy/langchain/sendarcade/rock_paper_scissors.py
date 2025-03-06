import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class RockPaperScissorsTool(BaseTool):
    name: str = "rock_paper_scissors"
    description: str = """
    Plays a game of Rock-Paper-Scissors using RockPaperScissorsManager by Send Arcade.

    Input: A JSON string with:
    {
        "amount" "float, The amount of SOL to stake.
        "choice": "string, the player's choice ('rock', 'paper', or 'scissors')"
    }
    Output:
    {
        "result": "string, the game result",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "amount": {"type": float, "required": True},
                "choice": {"type": str, "required": True, }
            }
            data = json.loads(input)
            validate_input(data, schema)
            result = await self.agent_kit.rock_paper_scissors(
                amount=data["amount"],
                choice=data["choice"]
            )
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error playing Rock-Paper-Scissors: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
