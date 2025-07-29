

from mcp.types import Tool

from agentipy.tools.burn_and_close_account import BurnManager
from agentipy.tools.deploy_token import TokenDeploymentManager
from agentipy.tools.get_balance import BalanceFetcher
from agentipy.tools.get_tps import SolanaPerformanceTracker
from agentipy.tools.transfer import TokenTransferManager

CORE_ACTIONS = {
    "GET_BALANCE": Tool(
        name="GET_BALANCE",
        description="Fetches wallet balance. input_schema Example: { token_address: string|undefined = undefined }",
        inputSchema={
            "token_address": {
                "type": "string",
                "description": "Optional token address"
            },
        },
        handler=lambda agent, params: BalanceFetcher.get_balance(agent, params.get("token_address")),
    ),
    "TRANSFER": Tool(
        name="TRANSFER",
        description="Transfers tokens. input_schema Example: { amount: number, mint: string|undefined = undefined, to: string }",
        inputSchema={
            "amount": {
                "type": "number",
                "description": "Amount to transfer"
            },
            "mint": {
                "type": "string",
                "description": "Optional SPL token mint address"
            },
            "to": {
                "type": "string",
                "description": "Recipient wallet address"
            },
        },
        handler=lambda agent, params: TokenTransferManager.transfer(
            agent,
            params["to"],
            params["amount"],
            params.get("mint")
        ),
    ),
    "DEPLOY_TOKEN": Tool(
        name="DEPLOY_TOKEN",
        description="Deploys a new SPL token. input_schema Example: { decimals: number = 9 }",
        inputSchema={
            "decimals": {
                "type": "integer",
                "description": "Number of decimals"
            },
        },
        handler=lambda agent, params: TokenDeploymentManager.deploy_token(agent, params.get("decimals", 9)),
    ),
    "GET_WALLET_ADDRESS": Tool(
        name="GET_WALLET_ADDRESS",
        description="Returns the public wallet address of the current agent. No input is required.",
        inputSchema={},
        handler=lambda agent, params: agent.get_wallet_address(),
    ),
    "BURN_AND_CLOSE_TOKEN_ACCOUNTS": Tool(
        name="BURN_AND_CLOSE_TOKEN_ACCOUNTS",
        description="Burns and closes the specified token account. input_schema Example: { token_account: string }",
        inputSchema={},
        handler=lambda agent, params: BurnManager.burn_and_close_account(
            agent,
            params["token_account"]
        ),
    ),
    "FETCH_CURRENT_TPS": Tool(
        name="FETCH_CURRENT_TPS",
        description="Fetches the current transactions per second (TPS) on the Solana network. No input is required.",
        inputSchema={},
        handler=lambda agent, params: SolanaPerformanceTracker.fetch_current_tps()
    )
}