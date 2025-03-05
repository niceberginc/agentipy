from agentipy.agent import SolanaAgentKit
from agentipy.langchain.lulo.lend import LuloLendTool
from agentipy.langchain.lulo.withdraw import LuloWithdrawTool

def get_lulo_tools(solana_kit: SolanaAgentKit):
    return [
        LuloLendTool(solana_kit=solana_kit),
        LuloWithdrawTool(solana_kit=solana_kit)
    ]