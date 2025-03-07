import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaCalculatePumpCurvePriceTool(BaseTool):
    name: str = "solana_calculate_pump_curve_price"
    description: str = """
    Calculate the price for a bonding curve based on its state.

    Input: A JSON string with:
    {
        "curve_state": "BondingCurveState object as a dictionary"
    }

    Output:
    {
        "status": "success",
        "price": "The calculated price"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "curve_state": {"type": str, "required": True}
            }
            validate_input(data, schema)

            curve_state = data["curve_state"]

            result = await self.solana_kit.calculate_pump_curve_price(curve_state)
            return {
                "status": "success",
                "price": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution.")
