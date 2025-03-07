from agentipy.agent import SolanaAgentKit
from agentipy.langchain.solutiofi.burn_accounts import SolutiofiBurnTokensTool
from agentipy.langchain.solutiofi.close_accounts import \
    SolutiofiCloseAccountsTool
from agentipy.langchain.solutiofi.merge_tokens import SolutiofiMergeTokensTool
from agentipy.langchain.solutiofi.spread_token import SolutiofiSpreadTokenTool


def get_solutiofi_tools(agent_kit: SolanaAgentKit):
    return [
        SolutiofiCloseAccountsTool(agent_kit=agent_kit),
        SolutiofiMergeTokensTool(agent_kit=agent_kit),
        SolutiofiSpreadTokenTool(agent_kit=agent_kit),
        SolutiofiBurnTokensTool(agent_kit=agent_kit)
    ]   