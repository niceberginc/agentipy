from agentipy.agent import SolanaAgentKit
from .bundles import SolanaGetBundleStatuses, SolanaSendBundle, SolanaGetInflightBundleStatuses

def get_bundles_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaGetBundleStatuses(solana_kit=solana_kit),
        SolanaSendBundle(solana_kit=solana_kit),
        SolanaGetInflightBundleStatuses(solana_kit=solana_kit)
    ]

