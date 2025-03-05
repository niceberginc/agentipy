from agentipy.agent import SolanaAgentKit
from agentipy.langchain.moonshot.buy import SolanaBuyUsingMoonshotTool
from agentipy.langchain.moonshot.sell import SolanaSellUsingMoonshotTool


def get_moonshot_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaSellUsingMoonshotTool(solana_kit=solana_kit),
        SolanaBuyUsingMoonshotTool(solana_kit=solana_kit)
    ]


