from agentipy.langchain.solayermanager.solayer_restake import SolayerRestakeTool
from agentipy.agent import SolanaAgentKit


def get_solayer_tools(agent_kit: SolanaAgentKit):
    return [
        SolayerRestakeTool(agent_kit=agent_kit)
    ]   