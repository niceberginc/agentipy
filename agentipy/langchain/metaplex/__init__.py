from agentipy.agent import SolanaAgentKit
from agentipy.langchain.metaplex.assets import SolanaGetMetaplexAssetTool
from agentipy.langchain.metaplex.collections import (
    SolanaDeployCollectionTool, SolanaGetMetaplexAssetsByAuthorityTool,
    SolanaGetMetaplexAssetsByCreatorTool)
from agentipy.langchain.metaplex.minting import SolanaMintMetaplexCoreNFTTool


def get_metaplex_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaMintMetaplexCoreNFTTool(solana_kit=solana_kit),
        SolanaGetMetaplexAssetTool(solana_kit=solana_kit),
        SolanaGetMetaplexAssetsByCreatorTool(solana_kit=solana_kit),
        SolanaDeployCollectionTool(solana_kit=solana_kit),
        SolanaGetMetaplexAssetsByAuthorityTool(solana_kit=solana_kit)
    ]

