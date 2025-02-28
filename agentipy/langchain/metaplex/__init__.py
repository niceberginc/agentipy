from agentipy.agent import SolanaAgentKit
from agentipy.langchain.metaplex.assets import SolanaGetMetaplexAssetTool
from agentipy.langchain.metaplex.collections import SolanaGetMetaplexAssetsByCreatorTool
from agentipy.langchain.metaplex.miniting import SolanaMintMetaplexCoreNFTTool


def get_metaplex_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaMintMetaplexCoreNFTTool(solana_kit=solana_kit),
        SolanaGetMetaplexAssetTool(solana_kit=solana_kit),
        SolanaGetMetaplexAssetsByCreatorTool(solana_kit=solana_kit),
    ]

