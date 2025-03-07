from agentipy.agent import SolanaAgentKit
from .vault import (
    GetDriftLendBorrowApyTool,
    CreateDriftVaultTool,
    UpdateDriftVaultDelegateTool,
    UpdateDriftVaultTool,
    GetDriftVaultInfoTool,
    DepositIntoDriftVaultTool,
    RequestWithdrawalFromDriftVaultTool,
    WithdrawFromDriftVaultTool,
    DeriveDriftVaultAddressTool,
    TradeUsingDelegatedDriftVaultTool
)
from .account import (
    CreateDriftUserAccountTool,
    DepositToDriftUserAccountTool,
    WithdrawFromDriftUserAccountTool,
    CheckIfDriftAccountExistsTool,
    DriftUserAccountInfoTool
)
from .market import (
    GetAvailableDriftMarketsTool,
    TradeUsingDriftPerpAccountTool,
    GetDriftPerpMarketFundingRateTool,
    GetDriftEntryQuoteOfPerpTradeTool,
    DriftSwapSpotTokenTool
)
from .insurance import (
    StakeToDriftInsuranceFundTool,
    RequestUnstakeFromDriftInsuranceFundTool,
    UnstakeFromDriftInsuranceFundTool
)

def get_drift_tools(solana_kit: SolanaAgentKit):
    
    return [
        # Vault tools
        GetDriftLendBorrowApyTool(solana_kit=solana_kit),
        CreateDriftVaultTool(solana_kit=solana_kit),
        UpdateDriftVaultDelegateTool(solana_kit=solana_kit),
        UpdateDriftVaultTool(solana_kit=solana_kit),
        GetDriftVaultInfoTool(solana_kit=solana_kit),
        DepositIntoDriftVaultTool(solana_kit=solana_kit),
        RequestWithdrawalFromDriftVaultTool(solana_kit=solana_kit),
        WithdrawFromDriftVaultTool(solana_kit=solana_kit),
        DeriveDriftVaultAddressTool(solana_kit=solana_kit),
        TradeUsingDelegatedDriftVaultTool(solana_kit=solana_kit),
        
        # Account tools
        CreateDriftUserAccountTool(solana_kit=solana_kit),
        DepositToDriftUserAccountTool(solana_kit=solana_kit),
        WithdrawFromDriftUserAccountTool(solana_kit=solana_kit),
        CheckIfDriftAccountExistsTool(solana_kit=solana_kit),
        DriftUserAccountInfoTool(solana_kit=solana_kit),
        
        # Market tools
        GetAvailableDriftMarketsTool(solana_kit=solana_kit),
        TradeUsingDriftPerpAccountTool(solana_kit=solana_kit),
        GetDriftPerpMarketFundingRateTool(solana_kit=solana_kit),
        GetDriftEntryQuoteOfPerpTradeTool(solana_kit=solana_kit),
        DriftSwapSpotTokenTool(solana_kit=solana_kit),
        
        # Insurance tools
        StakeToDriftInsuranceFundTool(solana_kit=solana_kit),
        RequestUnstakeFromDriftInsuranceFundTool(solana_kit=solana_kit),
        UnstakeFromDriftInsuranceFundTool(solana_kit=solana_kit)
    ]