from agentipy.agent import SolanaAgentKit
from agentipy.langchain.debridge.status import \
    SolanaDeBridgeCheckTransactionStatusTool
from agentipy.langchain.debridge.transaction import (
    SolanaDeBridgeCreateTransactionTool, SolanaDeBridgeExecuteTransactionTool)


def get_debridge_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaDeBridgeCreateTransactionTool(solana_kit=solana_kit),
        SolanaDeBridgeCheckTransactionStatusTool(solana_kit=solana_kit),
        SolanaDeBridgeExecuteTransactionTool(solana_kit=solana_kit),
    ]


