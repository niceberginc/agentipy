from agentipy.agent import SolanaAgentKit
from agentipy.langchain.tensor.trade import (TensorCancelListingTool,
                                             TensorListNFTForSaleTool)


def get_tensor_tools(solana_kit: SolanaAgentKit):
    return [
        TensorCancelListingTool(solana_kit),
        TensorListNFTForSaleTool(solana_kit),
    ]