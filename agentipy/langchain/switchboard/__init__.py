from agentipy.agent import SolanaAgentKit
from agentipy.langchain.switchboard.simulate_switchboard_feed import \
    SwitchboardSimulateFeedTool


def get_switchboard_tools(solana_kit: SolanaAgentKit):
    return [
        SwitchboardSimulateFeedTool(solana_kit=solana_kit)
    ]