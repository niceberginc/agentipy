from agentipy.agent import SolanaAgentKit
from agentipy.langchain.virtuals.prototype import (VirtualsBuyPrototypeTool,
                                                   VirtualsSellPrototypeTool)
from agentipy.langchain.virtuals.sentient import (
    VirtualsBuySentientTool, VirtualsGetSentientListingsTool,
    VirtualsSellSentientTool)


def get_solana_virtuals_tools(solana_kit: SolanaAgentKit):
    return [
        VirtualsBuyPrototypeTool(solana_kit=solana_kit),
        VirtualsSellPrototypeTool(solana_kit=solana_kit),
        VirtualsBuySentientTool(solana_kit=solana_kit),
        VirtualsGetSentientListingsTool(solana_kit=solana_kit),
        VirtualsSellSentientTool(solana_kit=solana_kit),
    ]