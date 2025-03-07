import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input
from solders.pubkey import Pubkey # type: ignore


class FluxBeamCreatePoolTool(BaseTool):
    name: str = "fluxbeam_create_pool"
    description: str = """
    Creates a new pool using FluxBeam with FluxBeamManager.

    Input: A JSON string with:
    {
        "token_a": "string, the mint address of the first token",
        "token_a_amount": "float, the amount to swap (in token decimals)",
        "token_b": "string, the mint address of the second token",
        "token_b_amount": "float, the amount to swap (in token decimals)"
    }
    Output:
    {
        "transaction_signature": "string, the transaction signature",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "token_a": {"type": str, "required": True},
                "token_a_amount": {"type": float, "required": True},
                "token_b": {"type": str, "required": True},
                "token_b_amount": {"type": float, "required": True}
            }
            validate_input(data, schema)
            transaction_signature = await self.agent_kit.fluxbeam_create_pool(
                token_a=Pubkey.from_string(data["token_a"]),
                token_a_amount=data["token_a_amount"],
                token_b=Pubkey.from_string(data["token_b"]),
                token_b_amount=data["token_b_amount"]
            )
            return {
                "transaction_signature": transaction_signature,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_signature": None,
                "message": f"Error creating pool using FluxBeam: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
