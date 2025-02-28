from agentipy.agent import SolanaAgentKit
from agentipy.langchain.orca.positions import (
    OrcaClosePositionTool,
    OrcaFetchPositionsTool,
    OrcaOpenCenteredPositionTool,
    OrcaOpenSingleSidedPositionTool
)
from agentipy.langchain.orca.clmm import OrcaCreateClmmTool
from agentipy.langchain.orca.liquidity_pool import OrcaCreateLiquidityPoolTool


def get_orca_tools(solana_kit: SolanaAgentKit):
    return [
        OrcaClosePositionTool(solana_kit=solana_kit),
        OrcaCreateClmmTool(solana_kit=solana_kit),
        OrcaCreateLiquidityPoolTool(solana_kit=solana_kit),
        OrcaFetchPositionsTool(solana_kit=solana_kit),
        OrcaOpenCenteredPositionTool(solana_kit=solana_kit),
        OrcaOpenSingleSidedPositionTool(solana_kit=solana_kit)
    ]