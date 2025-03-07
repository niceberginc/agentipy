from agentipy.agent import SolanaAgentKit

from .bundles import (SolanaGetBundleStatuses, SolanaGetInflightBundleStatuses,
                      SolanaSendBundle)
from .send_txn import SolanaSendTxn
from .tip import SolanaGetRandomTipAccount, SolanaGetTipAccounts


def get_jito_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaGetBundleStatuses(solana_kit=solana_kit),
        SolanaSendBundle(solana_kit=solana_kit),
        SolanaGetInflightBundleStatuses(solana_kit=solana_kit),
        SolanaGetTipAccounts(solana_kit=solana_kit),
        SolanaGetRandomTipAccount(solana_kit=solana_kit),
        SolanaSendTxn(solana_kit=solana_kit),
    ]

