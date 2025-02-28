import json
from langchain_core.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input
from solana.pubkey import Pubkey # type: ignore

class SolanaGetPumpCurveStateTool(BaseTool):
    name: str = "solana_get_pump_curve_state"
    description: str = """
    Get the pump curve state for a specific bonding curve.

    Input: A JSON string with:
    {
        "conn": "AsyncClient instance or connection object",
        "curve_address": "The public key of the bonding curve as a string"
    }

    Output:
    {
        "status": "success",
        "data": <PumpCurveState object as a dictionary>
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:    
            data = json.loads(input)
            schema = {
                "conn": {"type": str, "required": True},
                "curve_address": {"type": str, "required": True}
            }
            validate_input(data, schema)

            conn = data["conn"]
            curve_address = data["curve_address"]

            curve_address_key = Pubkey(curve_address)
            result = await self.solana_kit.get_pump_curve_state(conn, curve_address_key)
            return {
                "status": "success",
                "data": result.dict(),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution.")

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
