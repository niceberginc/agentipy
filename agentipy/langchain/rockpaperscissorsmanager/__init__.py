
from agentipy.agent import SolanaAgentKit
from .rock_paper_scissors import RockPaperScissorsTool

def get_rock_paper_scissors_tools(agent_kit: SolanaAgentKit):
    return [
        RockPaperScissorsTool(agent_kit=agent_kit)
    ]