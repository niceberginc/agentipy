import json
from agentipy.agent import SolanaAgentKit
from langchain.tools import BaseTool
from agentipy.helpers import validate_input

class SolanaGetBundleStatuses(BaseTool):
    name: str = "get_bundle_statuses"
    description: str = """
    Get the current statuses of specified Jito bundles.

    Input: A JSON string with:
    {
        "bundle_uuids": "List of bundle UUIDs"
    }

    Output:
    {
        "statuses": "List of corresponding bundle statuses"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "bundle_uuids": {"type": list, "required": True}
            }
            validate_input(data, schema)

            bundle_uuids = data["bundle_uuids"]
            result = await self.solana_kit.get_bundle_statuses(bundle_uuids)
            return {
                "statuses": result
            }
        except Exception as e:
            return {
                "statuses": None
            }

    def _run(self):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaSendBundle(BaseTool):
    name: str = "send_bundle"
    description: str = """
    Send a bundle of transactions to the Jito network for processing.

    Input: A JSON string with:
    {
        "txn_signatures": "List of transaction signatures"
    }

    Output:
    {
        "bundle_ids": "List of unique identifiers for the submitted bundles"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "txn_signatures": {"type": list, "required": True}
            }
            validate_input(data, schema)

            txn_signatures = data["txn_signatures"]
            result = await self.solana_kit.send_bundle(txn_signatures)
            return {
                "bundle_ids": result
            }
        except Exception as e:
            return {
                "bundle_ids": None
            }

    def _run(self):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaGetInflightBundleStatuses(BaseTool):
    name: str = "get_inflight_bundle_statuses"
    description: str = """
    Get the statuses of bundles that are currently in flight.

    Input: A JSON string with:
    {
        "bundle_uuids": "List of bundle UUIDs"
    }

    Output:
    {
        "statuses": "List of statuses corresponding to currently inflight bundles"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "bundle_uuids": {"type": list, "required": True}
            }
            validate_input(data, schema)

            bundle_uuids = data["bundle_uuids"]
            result = await self.solana_kit.get_inflight_bundle_statuses(bundle_uuids)
            return {
                "statuses": result
            }
        except Exception as e:
            return {
                "statuses": None
            }

    def _run(self):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )


