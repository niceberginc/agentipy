from typing import List

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit

from .shield import RentShieldCheckTokenTool, RentShieldScanWalletTool


def get_rentshield_tools(solana_kit: SolanaAgentKit) -> List[BaseTool]:
    return [
        RentShieldCheckTokenTool(agent_kit=solana_kit),
        RentShieldScanWalletTool(agent_kit=solana_kit),
    ]
