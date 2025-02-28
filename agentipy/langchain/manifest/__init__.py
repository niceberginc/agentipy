from agentipy.agent import SolanaAgentKit
from agentipy.langchain.manifest.market import (
    ManifestWithdrawAllTool,
    OpenBookCreateMarketTool
)
from agentipy.langchain.manifest.orders import (
    ManifestCreateMarketTool,
    ManifestPlaceLimitOrderTool,
    ManifestPlaceBatchOrdersTool,
  
)



def get_manifest_tools(solana_kit: SolanaAgentKit):
    return [
       
        ManifestWithdrawAllTool(solana_kit=solana_kit),
        OpenBookCreateMarketTool(solana_kit=solana_kit),
        ManifestCreateMarketTool(solana_kit=solana_kit),
        ManifestPlaceLimitOrderTool(solana_kit=solana_kit),
        ManifestPlaceBatchOrdersTool(solana_kit=solana_kit),
       
      
    ]