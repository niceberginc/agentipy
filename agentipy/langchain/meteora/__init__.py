from agentipy.agent import SolanaAgentKit
from agentipy.langchain.meteora.dlmm import SolanaMeteoraDLMMTool


def get_meteora_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaMeteoraDLMMTool(solana_kit=solana_kit)
    ]

