from agentipy.agent import SolanaAgentKit
from agentipy.langchain.voltr.deposit_strategy import VoltrDepositStrategyTool
from agentipy.langchain.voltr.get_position_values import \
    VoltrGetPositionValuesTool
from agentipy.langchain.voltr.withdraw_strategy import \
    VoltrWithdrawStrategyTool


def get_voltr_tools(solana_kit: SolanaAgentKit):
    return [
        VoltrDepositStrategyTool(solana_kit=solana_kit),
        VoltrGetPositionValuesTool(solana_kit=solana_kit),
        VoltrWithdrawStrategyTool(solana_kit=solana_kit),
    ]