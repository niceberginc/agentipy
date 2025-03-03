from agentipy.agent import SolanaAgentKit
from agentipy.langchain.fluxbeam.create_pool import FluxBeamCreatePoolTool

def get_fluxbeam_tools(solana_kit: SolanaAgentKit):
    return [
        FluxBeamCreatePoolTool(solana_kit=solana_kit)
    ]
