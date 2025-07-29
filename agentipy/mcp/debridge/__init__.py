from mcp.types import Tool

from agentipy.tools.use_debridge import DeBridgeManager

DEBRIDGE_ACTIONS = {
    "CREATE_DEBRIDGE_TRANSACTION": Tool(
        name="CREATE_DEBRIDGE_TRANSACTION",
        description=(
            "Create a cross-chain bridge transaction using deBridge Liquidity Network API. "
            "input_schema Example: { src_chain_id: string, src_chain_token_in: string, src_chain_token_in_amount: string, "
            "dst_chain_id: string, dst_chain_token_out: string, dst_chain_token_out_recipient: string, "
            "src_chain_order_authority_address: string, dst_chain_order_authority_address: string, "
            "affiliate_fee_percent: string = '0', affiliate_fee_recipient: string|undefined = undefined, prepend_operating_expenses: boolean = true, "
            "dst_chain_token_out_amount: string = 'auto' }"
        ),
        inputSchema={
            "src_chain_id": {"type": "string", "description": "The internal chain ID of the source chain."},
            "src_chain_token_in": {"type": "string", "description": "The address of the input token (token being sold)."},
            "src_chain_token_in_amount": {
                "type": "string",
                "description": "The amount of input token to sell (with decimals), or 'auto'.",
            },
            "dst_chain_id": {"type": "string", "description": "The internal chain ID of the destination chain."},
            "dst_chain_token_out": {"type": "string", "description": "The address of the output token (token being bought)."},
            "dst_chain_token_out_recipient": {"type": "string", "description": "The recipient address on the destination chain."},
            "src_chain_order_authority_address": {"type": "string", "description": "The address on the source chain for order authority."},
            "dst_chain_order_authority_address": {"type": "string", "description": "The address on the destination chain for order authority."},
            "affiliate_fee_percent": {"type": "string", "description": "The percentage of affiliate fee to cut off. Defaults to '0'."},
            "affiliate_fee_recipient": {"type": "string", "description": "The recipient address of the affiliate fee. Optional."},
            "prepend_operating_expenses": {"type": "boolean", "description": "Whether to prepend operating expenses. Defaults to True."},
            "dst_chain_token_out_amount": {
                "type": "string",
                "description": "The amount of output token to buy (with decimals), or 'auto'. Defaults to 'auto'.",
            },
        },
        handler=lambda agent, params: DeBridgeManager.create_debridge_transaction(
            agent,
            src_chain_id=params["src_chain_id"],
            src_chain_token_in=params["src_chain_token_in"],
            src_chain_token_in_amount=params["src_chain_token_in_amount"],
            dst_chain_id=params["dst_chain_id"],
            dst_chain_token_out=params["dst_chain_token_out"],
            dst_chain_token_out_recipient=params["dst_chain_token_out_recipient"],
            src_chain_order_authority_address=params["src_chain_order_authority_address"],
            dst_chain_order_authority_address=params["dst_chain_order_authority_address"],
            affiliate_fee_percent=params["affiliate_fee_percent"],
            affiliate_fee_recipient=params["affiliate_fee_recipient"],
            prepend_operating_expenses=params["prepend_operating_expenses"],
            dst_chain_token_out_amount=params["dst_chain_token_out_amount"],
        ),
    ),

    "EXECUTE_DEBRIDGE_TRANSACTION": Tool(
        name="EXECUTE_DEBRIDGE_TRANSACTION",
        description="Execute a cross-chain bridge transaction using deBridge Liquidity Network API. input_schema Example: { transaction_data: { data: string } }",
        inputSchema={
            "transaction_data": {
                "type": "object",
                "description": "The transaction object returned by the bridge API. Must contain a 'data' field (base64).",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "Base64-encoded transaction to execute.",
                    }
                },
                "required": ["data"],
            },
        },
        handler=lambda agent, params: DeBridgeManager.execute_debridge_transaction(
            agent,
            transaction_data=params["transaction_data"],
        ),
    ),

    "CHECK_TRANSACTION_STATUS": Tool(
        name="CHECK_TRANSACTION_STATUS",
        description="Check the status of a cross-chain bridge transaction using deBridge Liquidity Network API. input_schema Example: { tx_hash: string }",
        inputSchema={
            "tx_hash": {
                "type": "string",
                "description": "The transaction hash to check the status for.",
            },
        },
        handler=lambda agent, params: DeBridgeManager.check_transaction_status(
            agent,
            tx_hash=params["tx_hash"],
        ),
    ),
}
