

from agentipy.agent import SolanaAgentKit
from agentipy.langchain.pumpfun.buy_token import SolanaBuyPumpfunTokenTool
from agentipy.langchain.pumpfun.launch_token import SolanaPumpFunTokenTool
from agentipy.langchain.pumpfun.sell_token import SolanaSellPumpfunTokenTool


def get_pumpfun_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaPumpFunTokenTool(solana_kit=solana_kit),
        SolanaBuyPumpfunTokenTool(solana_kit=solana_kit),
        SolanaSellPumpfunTokenTool(solana_kit=solana_kit)
    ]
