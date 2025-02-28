import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaDeBridgeCreateTransactionTool(BaseTool):
    name: str = "debridge_create_transaction"
    description: str = """
    Creates a transaction for bridging assets across chains using DeBridge.

    Input: A JSON string with:
    {
        "src_chain_id": "string, the source chain ID",
        "src_chain_token_in": "string, the token address on the source chain",
        "src_chain_token_in_amount": "string, the token amount to send on the source chain",
        "dst_chain_id": "string, the destination chain ID",
        "dst_chain_token_out": "string, the token address on the destination chain",
        "dst_chain_token_out_recipient": "string, the recipient address on the destination chain",
        "src_chain_order_authority_address": "string, source chain order authority address",
        "dst_chain_order_authority_address": "string, destination chain order authority address",
        "affiliate_fee_percent": "string, optional, affiliate fee percent (default: '0')",
        "affiliate_fee_recipient": "string, optional, affiliate fee recipient address",
        "prepend_operating_expenses": "bool, optional, whether to prepend operating expenses (default: True)",
        "dst_chain_token_out_amount": "string, optional, amount of destination chain tokens out (default: 'auto')"
    }

    Output:
    {
        "transaction_data": "dict, the transaction data",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "src_chain_id": {"type": str, "required": True},
                "src_chain_token_in": {"type": str, "required": True},
                "src_chain_token_in_amount": {"type": str, "required": True},
                "dst_chain_id": {"type": str, "required": True},
                "dst_chain_token_out": {"type": str, "required": True},
                "dst_chain_token_out_recipient": {"type": str, "required": True},
                "src_chain_order_authority_address": {"type": str, "required": True},
                "dst_chain_order_authority_address": {"type": str, "required": True},
                "affiliate_fee_percent": {"type": str, "required": False},
                "affiliate_fee_recipient": {"type": str, "required": False},
                "prepend_operating_expenses": {"type": bool, "required": False},
                "dst_chain_token_out_amount": {"type": str, "required": False}
            }
            validate_input(data, schema)

            transaction_data = await self.solana_kit.create_debridge_transaction(
                src_chain_id=data["src_chain_id"],
                src_chain_token_in=data["src_chain_token_in"],
                src_chain_token_in_amount=data["src_chain_token_in_amount"],
                dst_chain_id=data["dst_chain_id"],
                dst_chain_token_out=data["dst_chain_token_out"],
                dst_chain_token_out_recipient=data["dst_chain_token_out_recipient"],
                src_chain_order_authority_address=data["src_chain_order_authority_address"],
                dst_chain_order_authority_address=data["dst_chain_order_authority_address"],
                affiliate_fee_percent=data.get("affiliate_fee_percent", "0"),
                affiliate_fee_recipient=data.get("affiliate_fee_recipient", ""),
                prepend_operating_expenses=data.get("prepend_operating_expenses", True),
                dst_chain_token_out_amount=data.get("dst_chain_token_out_amount", "auto")
            )
            return {
                "transaction_data": transaction_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_data": None,
                "message": f"Error creating DeBridge transaction: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaDeBridgeExecuteTransactionTool(BaseTool):
    name: str = "debridge_execute_transaction"
    description: str = """
    Executes a prepared DeBridge transaction.

    Input: A JSON string with:
    {
        "transaction_data": "dict, the prepared transaction data"
    }

    Output:
    {
        "result": "dict, the result of transaction execution",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "transaction_data": {"type": dict, "required": True}
            }
            validate_input(data, schema)

            transaction_data = data["transaction_data"]

            result = await self.solana_kit.execute_debridge_transaction(transaction_data)
            return {
                "result": result,
                "message": "Success"
            }
        except Exception as e:
            return {
                "result": None,
                "message": f"Error executing DeBridge transaction: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
