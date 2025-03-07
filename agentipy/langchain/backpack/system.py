import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class BackpackGetStatusTool(BaseTool):
    name: str = "backpack_get_status"
    description: str = """
    Fetches the system status and any status messages using the BackpackManager.

    Input: None
    Output:
    {
        "status": "dict, the system status",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            status = await self.solana_kit.get_status()
            return {
                "status": status,
                "message": "Success"
            }
        except Exception as e:
            return {
                "status": None,
                "message": f"Error fetching system status: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackSendPingTool(BaseTool):
    name: str = "backpack_send_ping"
    description: str = """
    Sends a ping and expects a "pong" response using the BackpackManager.

    Input: None
    Output:
    {
        "response": "string, the response ('pong')",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            response = await self.solana_kit.send_ping()
            return {
                "response": response,
                "message": "Success"
            }
        except Exception as e:
            return {
                "response": None,
                "message": f"Error sending ping: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetSystemTimeTool(BaseTool):
    name: str = "backpack_get_system_time"
    description: str = """
    Fetches the current system time using the BackpackManager.

    Input: None
    Output:
    {
        "system_time": "string, the current system time",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            system_time = await self.solana_kit.get_system_time()
            return {
                "system_time": system_time,
                "message": "Success"
            }
        except Exception as e:
            return {
                "system_time": None,
                "message": f"Error fetching system time: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetSupportedAssetsTool(BaseTool):
    name: str = "backpack_get_supported_assets"
    description: str = """
    Fetches supported assets using the BackpackManager.

    Input: None
    Output:
    {
        "assets": "list, the supported assets",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            assets = await self.solana_kit.get_supported_assets()
            return {
                "assets": assets,
                "message": "Success"
            }
        except Exception as e:
            return {
                "assets": None,
                "message": f"Error fetching supported assets: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetTickerInformationTool(BaseTool):
    name: str = "backpack_get_ticker_information"
    description: str = """
    Fetches ticker information using the BackpackManager.

    Input: A JSON string with optional filters for the query.
    Output:
    {
        "ticker_information": "dict, the ticker information",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            ticker_info = await self.solana_kit.get_ticker_information(**data)
            return {
                "ticker_information": ticker_info,
                "message": "Success"
            }
        except Exception as e:
            return {
                "ticker_information": None,
                "message": f"Error fetching ticker information: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class BackpackGetCollateralInfoTool(BaseTool):
    name: str = "backpack_get_collateral_info"
    description: str = """
    Fetches collateral information using the BackpackManager.

    Input: A JSON string with:
    {
        "sub_account_id": "int, optional, the sub-account ID for collateral information"
    }
    Output:
    {
        "collateral_info": "dict, the collateral information",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "sub_account_id": {"type": int, "required": False}
            }
            data = json.loads(input)
            validate_input(data, schema)

            collateral_info = await self.solana_kit.get_collateral_info(
                sub_account_id=data.get("sub_account_id")
            )
            return {
                "collateral_info": collateral_info,
                "message": "Success"
            }
        except Exception as e:
            return {
                "collateral_info": None,
                "message": f"Error fetching collateral information: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
