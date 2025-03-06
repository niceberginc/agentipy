import json

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class OrcaFetchPositionsTool(BaseTool):
    name: str = "orca_fetch_positions"
    description: str = """
    Fetches all open positions using OrcaManager.

    Input: None
    Output:
    {
        "positions": "dict, details of all positions",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            positions = await self.solana_kit.fetch_positions()
            return {
                "positions": positions,
                "message": "Success"
            }
        except Exception as e:
            return {
                "positions": None,
                "message": f"Error fetching positions: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class OrcaOpenCenteredPositionTool(BaseTool):
    name: str = "orca_open_centered_position"
    description: str = """
    Opens a centered position using OrcaManager.

    Input: A JSON string with:
    {
        "whirlpool_address": "string, the Whirlpool address",
        "price_offset_bps": "int, the price offset in basis points",
        "input_token_mint": "string, the mint address of the input token",
        "input_amount": "float, the input token amount"
    }
    Output:
    {
        "position_data": "dict, details of the opened position",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "whirlpool_address": {"type": str, "required": True},
                "price_offset_bps": {"type": int, "required": True},
                "input_token_mint": {"type": str, "required": True},
                "input_amount": {"type": float, "required": True}
            }
            validate_input(data, schema)
            position_data = await self.solana_kit.open_centered_position(
                whirlpool_address=data["whirlpool_address"],
                price_offset_bps=data["price_offset_bps"],
                input_token_mint=data["input_token_mint"],
                input_amount=data["input_amount"]
            )
            return {
                "position_data": position_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "position_data": None,
                "message": f"Error opening centered position: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class OrcaOpenSingleSidedPositionTool(BaseTool):
    name: str = "orca_open_single_sided_position"
    description: str = """
    Opens a single-sided position using OrcaManager.

    Input: A JSON string with:
    {
        "whirlpool_address": "string, the Whirlpool address",
        "distance_from_current_price_bps": "int, the distance from the current price in basis points",
        "width_bps": "int, the width in basis points",
        "input_token_mint": "string, the mint address of the input token",
        "input_amount": "float, the input token amount"
    }
    Output:
    {
        "position_data": "dict, details of the opened position",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "whirlpool_address": {"type": str, "required": True},
                "distance_from_current_price_bps": {"type": int, "required": True},
                "width_bps": {"type": int, "required": True},
                "input_token_mint": {"type": str, "required": True},
                "input_amount": {"type": float, "required": True}
            }
            validate_input(data, schema)
            position_data = await self.solana_kit.open_single_sided_position(
                whirlpool_address=data["whirlpool_address"],
                distance_from_current_price_bps=data["distance_from_current_price_bps"],
                width_bps=data["width_bps"],
                input_token_mint=data["input_token_mint"],
                input_amount=data["input_amount"]
            )
            return {
                "position_data": position_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "position_data": None,
                "message": f"Error opening single-sided position: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


class OrcaClosePositionTool(BaseTool):
    name: str = "orca_close_position"
    description: str = """
    Closes a position using OrcaManager.

    Input: A JSON string with:
    {
        "position_mint_address": "string, the mint address of the position"
    }
    Output:
    {
        "closure_result": "dict, details of the closed position",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "position_mint_address": {"type": str, "required": True}
            }
            validate_input(data, schema)
            closure_result = await self.solana_kit.close_position(
                position_mint_address=data["position_mint_address"]
            )
            return {
                "closure_result": closure_result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "closure_result": None,
                "message": f"Error closing position: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
