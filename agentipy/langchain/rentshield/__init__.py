from agentipy.agent import SolanaAgentKit
from agentipy.langchain.rentshield.shield import (
    RentShieldCheckTokenTool,
    RentShieldScanWalletTool,
)


def get_rentshield_tools(solana_kit: SolanaAgentKit):
    return [
        RentShieldCheckTokenTool(agent_kit=solana_kit),
        RentShieldScanWalletTool(agent_kit=solana_kit),
    ]
