import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaHeliusCreateWebhookTool(BaseTool):
    name: str = "solana_helius_create_webhook"
    description: str = """
    Create a webhook for transaction events.

    Input: A JSON string with:
    {
        "webhook_url": "URL to send the webhook data",
        "transaction_types": "List of transaction types to listen for",
        "account_addresses": "List of account addresses to monitor",
        "webhook_type": "Type of webhook",
        "txn_status": "optional, transaction status to filter by",
        "auth_header": "optional, authentication header for the webhook"
    }

    Output:
    {
        "status": "success",
        "data": "Webhook creation response"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "webhook_url": {"type": str, "required": True},
                "transaction_types": {"type": list, "required": True},
                "account_addresses": {"type": list, "required": True},
                "webhook_type": {"type": str, "required": True},
                "auth_header": {"type": str, "required": False}
            }
            validate_input(data, schema)

            webhook_url = data["webhook_url"]
            transaction_types = data["transaction_types"]
            account_addresses = data["account_addresses"]
            webhook_type = data["webhook_type"]
            txn_status = data.get("txn_status", "all")
            auth_header = data.get("auth_header", None)

            result = await self.solana_kit.create_webhook(
                webhook_url, transaction_types, account_addresses, webhook_type, txn_status, auth_header
            )
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaHeliusGetAllWebhooksTool(BaseTool):
    name: str = "solana_helius_get_all_webhooks"
    description: str = """
    Fetch all webhooks created in the system.

    Input: None (No parameters required)

    Output:
    {
        "status": "success",
        "data": "List of all webhooks"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            result = await self.solana_kit.get_all_webhooks()
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaHeliusGetWebhookTool(BaseTool):
    name: str = "solana_helius_get_webhook"
    description: str = """
    Retrieve a specific webhook by ID.

    Input: A JSON string with:
    {
        "webhook_id": "ID of the webhook to retrieve"
    }

    Output:
    {
        "status": "success",
        "data": "Webhook details"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "webhook_id": {"type": str, "required": True}
            }
            validate_input(data, schema)
            webhook_id = data["webhook_id"]
            result = await self.solana_kit.get_webhook(webhook_id)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
class SolanaHeliusEditWebhookTool(BaseTool):
    name: str = "solana_helius_edit_webhook"
    description: str = """
    Edit an existing webhook by its ID.

    Input: A JSON string with:
    {
        "webhook_id": "ID of the webhook to edit",
        "webhook_url": "Updated URL for the webhook",
        "transaction_types": "Updated list of transaction types",
        "account_addresses": "Updated list of account addresses",
        "webhook_type": "Updated webhook type",
        "txn_status": "optional, updated transaction status filter",
        "auth_header": "optional, updated authentication header"
    }

    Output:
    {
        "status": "success",
        "data": "Updated webhook details"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "webhook_id": {"type": str, "required": True},
                "webhook_url": {"type": str, "required": True},
                "transaction_types": {"type": list, "required": True},
                "account_addresses": {"type": list, "required": True},
                "webhook_type": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
         
            webhook_id = data["webhook_id"]
            webhook_url = data["webhook_url"]
            transaction_types = data["transaction_types"]
            account_addresses = data["account_addresses"]
            webhook_type = data["webhook_type"]
            txn_status = data.get("txn_status", "all")
            auth_header = data.get("auth_header", None)

            result = await self.solana_kit.edit_webhook(
                webhook_id, webhook_url, transaction_types, account_addresses, webhook_type, txn_status, auth_header
            )
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaHeliusDeleteWebhookTool(BaseTool):
    name: str = "solana_helius_delete_webhook"
    description: str = """
    Delete a webhook by its ID.

    Input: A JSON string with:
    {
        "webhook_id": "ID of the webhook to delete"
    }

    Output:
    {
        "status": "success",
        "data": "Webhook deletion confirmation"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            schema = {
                "webhook_id": {"type": str, "required": True}
            }
            data = json.loads(input)
            validate_input(data, schema)
            webhook_id = data["webhook_id"] 
            result = await self.solana_kit.delete_webhook(webhook_id)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self):
        """Synchronous version of the run method, required by BaseTool."""
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

