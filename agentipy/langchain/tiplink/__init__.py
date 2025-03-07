from agentipy.agent import SolanaAgentKit
from agentipy.langchain.tiplink.create_tiplink import TiplinkCreateTool


def get_tiplink_tools(solana_kit: SolanaAgentKit):
    return [
        TiplinkCreateTool(solana_kit=solana_kit),
    ]