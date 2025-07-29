
from mcp.types import Tool

from agentipy.tools.use_jito import JitoManager

JITO_ACTIONS = {
    "GET_TIP_ACCOUNTS": Tool(
        name="GET_TIP_ACCOUNTS",
        description="Get the tip accounts from Jito.  No input is required.",
        inputSchema={},
        handler=lambda agent, params: JitoManager.get_tip_accounts(agent),
    ),
    "GET_RANDOM_TIP_ACCOUNT": Tool(
        name="GET_RANDOM_TIP_ACCOUNT",
        description="Get a random tip account from Jito.  No input is required.",
        inputSchema={},
        handler=lambda agent, params: JitoManager.get_random_tip_account(),
    ),
    "GET_BUNDLE_STATUSES": Tool(
        name="GET_BUNDLE_STATUSES",
        description="Get the status of a bundle from Jito. input_schema Example: { bundle_uuids: array }",
        inputSchema={"bundle_uuids": {"type": "array", "items": {"type": "string"}}},
        handler=lambda agent, params: JitoManager.get_bundle_statuses(agent, params["bundle_uuids"]),
    ),
    "SEND_BUNDLE": Tool(
        name="SEND_BUNDLE",
        description="Send a bundle to Jito. input_schema Example: { params: object }",
        inputSchema={"params": {"type": "object"}},
        handler=lambda agent, params: JitoManager.send_bundle(agent, params["params"]),
    ),
    "GET_INFLIGHT_BUNDLE_STATUSES": Tool(
        name="GET_INFLIGHT_BUNDLE_STATUSES",
        description="Get the status of inflight bundles from Jito. input_schema Example: { bundle_uuids: array }",
        inputSchema={"bundle_uuids": {"type": "array", "items": {"type": "string"}}},
        handler=lambda agent, params: JitoManager.get_inflight_bundle_statuses(agent, params["bundle_uuids"]),
    ),
    "SEND_TXN": Tool(
        name="SEND_TXN",
        description="Send a transaction using Jito. input_schema Example: { params: object }",
        inputSchema={"params": {"type": "object"}},
        handler=lambda agent, params: JitoManager.send_bundle(agent, params["params"]),
    ),
}