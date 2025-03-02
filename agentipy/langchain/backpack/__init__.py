from agentipy.agent import SolanaAgentKit

from .account import (
    BackpackGetAccountBalancesTool,
    BackpackGetAccountSettingsTool,
    BackpackUpdateAccountSettingsTool,
    BackpackGetAccountDepositsTool,
  
)
from .market import (
    BackpackGetMarketsTool,
    BackpackGetMarketTool,
    BackpackGetTickersTool,
    BackpackGetDepthTool,
    BackpackGetKlinesTool,
    BackpackGetMarkPriceTool,
    BackpackGetOpenInterestTool,
    BackpackGetFundingIntervalRatesTool,
   
)
from .orders import (
    BackpackGetOpenOrdersTool,
    BackpackExecuteOrderTool,
    BackpackCancelOpenOrderTool,
    BackpackCancelOpenOrdersTool,
    BackpackGetUsersOpenOrdersTool
)
from .positions import (
    BackpackGetOpenPositionsTool,
    BackpackGetBorrowLendPositionsTool,
    BackpackExecuteBorrowLendTool,
    BackpackGetBorrowHistoryTool,
    BackpackGetInterestHistoryTool
)
from .system import (
    BackpackGetStatusTool,
    BackpackSendPingTool,
    BackpackGetSystemTimeTool,
    BackpackGetSupportedAssetsTool,
    BackpackGetTickerInformationTool,
    BackpackGetCollateralInfoTool
)
from .history import (
    BackpackGetFillHistoryTool,
    BackpackGetBorrowPositionHistoryTool,
    BackpackGetFundingPaymentsTool,
    BackpackGetOrderHistoryTool,
    BackpackGetPnlHistoryTool,
    BackpackGetSettlementHistoryTool
)


def get_backpack_tools(solana_kit: SolanaAgentKit):
    """Returns a list of all available Backpack tools.
    
    Args:
        solana_kit (SolanaAgentKit): The Solana agent kit instance
        
    Returns:
        list: A list of all Backpack tools initialized with the provided solana_kit
    """
    
    return [
        # Account tools
        BackpackGetAccountBalancesTool(solana_kit),
        BackpackGetAccountSettingsTool(solana_kit),
        BackpackUpdateAccountSettingsTool(solana_kit),
        BackpackGetAccountDepositsTool(solana_kit),

        
        # Market tools
        BackpackGetMarketsTool(solana_kit),
        BackpackGetMarketTool(solana_kit),
        BackpackGetTickersTool(solana_kit),
        BackpackGetDepthTool(solana_kit),
        BackpackGetKlinesTool(solana_kit),
        BackpackGetMarkPriceTool(solana_kit),
        BackpackGetOpenInterestTool(solana_kit),
        BackpackGetFundingIntervalRatesTool(solana_kit),
        
        # Order tools
        BackpackGetOpenOrdersTool(solana_kit),
        BackpackExecuteOrderTool(solana_kit),
        BackpackCancelOpenOrderTool(solana_kit),
        BackpackCancelOpenOrdersTool(solana_kit),
        BackpackGetUsersOpenOrdersTool(solana_kit),
        
        # Position tools
        BackpackGetOpenPositionsTool(solana_kit),
        BackpackGetBorrowLendPositionsTool(solana_kit),
        BackpackExecuteBorrowLendTool(solana_kit),
        BackpackGetBorrowHistoryTool(solana_kit),
        BackpackGetInterestHistoryTool(solana_kit),
        
        # System tools
        BackpackGetStatusTool(solana_kit),
        BackpackSendPingTool(solana_kit),
        BackpackGetSystemTimeTool(solana_kit),
        BackpackGetSupportedAssetsTool(solana_kit),
        BackpackGetTickerInformationTool(solana_kit),
        BackpackGetCollateralInfoTool(solana_kit),
        
        # History tools
        BackpackGetFillHistoryTool(solana_kit),
        BackpackGetBorrowPositionHistoryTool(solana_kit),
        BackpackGetFundingPaymentsTool(solana_kit),
        BackpackGetOrderHistoryTool(solana_kit),
        BackpackGetPnlHistoryTool(solana_kit),
        BackpackGetSettlementHistoryTool(solana_kit)
    ]