from agentipy.agent import SolanaAgentKit
from agentipy.langchain.gibwork.create_task import SolanaCreateGibworkTaskTool


def get_gibwork_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaCreateGibworkTaskTool(solana_kit=solana_kit)
    ]


