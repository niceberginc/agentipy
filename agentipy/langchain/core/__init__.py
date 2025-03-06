from agentipy.agent import SolanaAgentKit
from agentipy.langchain.core.balance import SolanaBalanceTool
from agentipy.langchain.core.burn_and_close import SolanaBurnAndCloseTool
from agentipy.langchain.core.burn_and_close_multiple import \
    SolanaBurnAndCloseMultipleTool
from agentipy.langchain.core.create_image import SolanaCreateImageTool
from agentipy.langchain.core.data import (SolanaTokenDataByTickerTool,
                                          SolanaTokenDataTool)
from agentipy.langchain.core.deploy_token import SolanaDeployTokenTool
from agentipy.langchain.core.fetch_price import SolanaFetchPriceTool
from agentipy.langchain.core.get_wallet_address import \
    SolanaGetWalletAddressTool
from agentipy.langchain.core.report import (SolanaFetchTokenDetailedReportTool,
                                            SolanaFetchTokenReportSummaryTool)
from agentipy.langchain.core.stake import SolanaStakeTool
from agentipy.langchain.core.tps_calculator import SolanaTPSCalculatorTool
from agentipy.langchain.core.trade import SolanaTradeTool
from agentipy.langchain.core.transfer import SolanaTransferTool


def get_all_core_tools(solana_kit: SolanaAgentKit) -> list:
    """Get all core Solana tools initialized with the provided SolanaAgentKit.
    
    Args:
        solana_kit (SolanaAgentKit): The Solana agent kit to initialize tools with
        
    Returns:
        list: List of initialized Solana tools
    """
    return [
        SolanaBalanceTool(solana_kit=solana_kit),
        SolanaCreateImageTool(solana_kit=solana_kit),
        SolanaDeployTokenTool(solana_kit=solana_kit),
        SolanaTradeTool(solana_kit=solana_kit),
       
        SolanaStakeTool(solana_kit=solana_kit),
        SolanaGetWalletAddressTool(solana_kit=solana_kit),
        SolanaTPSCalculatorTool(solana_kit=solana_kit),
        SolanaFetchPriceTool(solana_kit=solana_kit),
        SolanaTokenDataTool(solana_kit=solana_kit),
        SolanaTokenDataByTickerTool(solana_kit=solana_kit),
        SolanaFetchTokenReportSummaryTool(solana_kit=solana_kit),
        SolanaFetchTokenDetailedReportTool(solana_kit=solana_kit),
        SolanaTransferTool(solana_kit=solana_kit),
        SolanaBurnAndCloseTool(solana_kit=solana_kit),
        SolanaBurnAndCloseMultipleTool(solana_kit=solana_kit),
    ]