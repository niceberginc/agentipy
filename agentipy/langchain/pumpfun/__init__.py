

from agentipy.agent import SolanaAgentKit
from agentipy.langchain.pumpfun.lunch_token import SolanaPumpFunTokenTool


def get_pumpfun_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaPumpFunTokenTool(solana_kit=solana_kit)
    ]
