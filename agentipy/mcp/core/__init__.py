

from mcp.types import Tool

from agentipy.tools.deploy_token import TokenDeploymentManager
from agentipy.tools.get_balance import BalanceFetcher
from agentipy.tools.transfer import TokenTransferManager

SOLANA_ACTIONS = {
    "GET_BALANCE": Tool(
        name="GET_BALANCE",
        description="Fetches wallet balance",
        inputSchema={"token_address": {"type": "string", "description": "Optional token address"}},
        handler=lambda agent, params: BalanceFetcher.get_balance(agent, params.get("token_address")),
    ),
    "TRANSFER": Tool(
        name="TRANSFER",
        description="Transfers tokens",
        inputSchema={
            "amount": {"type": "number", "description": "Amount to transfer"},
            "mint": {"type": "string", "description": "Optional SPL token mint address"},
            "to": {"type": "string", "description": "Recipient wallet address"},
        },
        handler=lambda agent, params: TokenTransferManager.transfer(agent, params["to"], params["amount"], params.get("mint")),
    ),
    "DEPLOY_TOKEN": Tool(
        name="DEPLOY_TOKEN",
        description="Deploys a new SPL token",
        inputSchema={"decimals": {"type": "integer", "description": "Number of decimals"}},
        handler=lambda agent, params: TokenDeploymentManager.deploy_token(agent, params.get("decimals", 9)),
    ),
}
