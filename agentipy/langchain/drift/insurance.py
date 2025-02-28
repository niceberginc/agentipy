import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class StakeToDriftInsuranceFundTool(BaseTool):
    name: str = "stake_to_drift_insurance_fund"
    description: str = """
    Stakes funds into the Drift insurance fund.

    Input: A JSON string with:
    {
        "amount": "float, amount to stake",
        "symbol": "string, token symbol"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "amount": {"type": float, "required": True},
                "symbol": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            
            transaction = await self.solana_kit.stake_to_drift_insurance_fund(
                amount=data["amount"],
                symbol=data["symbol"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error staking to Drift insurance fund: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class RequestUnstakeFromDriftInsuranceFundTool(BaseTool):
    name: str = "request_unstake_from_drift_insurance_fund"
    description: str = """
    Requests unstaking from the Drift insurance fund.

    Input: A JSON string with:
    {
        "amount": "float, amount to unstake",
        "symbol": "string, token symbol"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "amount": {"type": float, "required": True},
                "symbol": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
         
            transaction = await self.solana_kit.request_unstake_from_drift_insurance_fund(
                amount=data["amount"],
                symbol=data["symbol"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error requesting unstake from Drift insurance fund: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")

class UnstakeFromDriftInsuranceFundTool(BaseTool):
    name: str = "unstake_from_drift_insurance_fund"
    description: str = """
    Completes an unstaking request from the Drift insurance fund.

    Input: A JSON string with:
    {
        "symbol": "string, token symbol"
    }
    Output:
    {
        "transaction": "dict, transaction details",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "symbol": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
           
            transaction = await self.solana_kit.unstake_from_drift_insurance_fund(
                symbol=data["symbol"]
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error unstaking from Drift insurance fund: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError("This tool only supports async execution via _arun.")


