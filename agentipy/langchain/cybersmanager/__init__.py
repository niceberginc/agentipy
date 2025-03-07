from agentipy.agent import SolanaAgentKit
from agentipy.langchain.cybersmanager.create_coin import SolanaCybersCreateCoinTool


def get_cyber_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaCybersCreateCoinTool(solana_kit=solana_kit),
    ]  