from agentipy.agent import SolanaAgentKit
from agentipy.langchain.lulo.lend import LuloLendAssetsTool, LuloLendTool
from agentipy.langchain.lulo.withdraw import LuloWithdrawTool


def get_lulo_tools(solana_kit: SolanaAgentKit):
    return [
        LuloLendTool(agent_kit=solana_kit),
        LuloWithdrawTool(agent_kit=solana_kit),
        LuloLendAssetsTool(agent_kit=solana_kit)
    ]