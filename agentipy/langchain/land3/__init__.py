from agentipy.agent import SolanaAgentKit
from agentipy.langchain.land3.land_collection import Create3LandCollectionTool
from agentipy.langchain.land3.land_nft import Create3LandNFTTool




def get_land_tools(solana_kit: SolanaAgentKit):
    return [
        Create3LandCollectionTool(solana_kit=solana_kit),
        Create3LandNFTTool(solana_kit=solana_kit)
    ]


