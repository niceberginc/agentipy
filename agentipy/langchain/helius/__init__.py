from agentipy.agent import SolanaAgentKit
from agentipy.langchain.helius.active_listings import \
    SolanaHeliusGetActiveListingsTool
from agentipy.langchain.helius.address_name import \
    SolanaHeliusGetAddressNameTool
from agentipy.langchain.helius.balances import SolanaHeliusGetBalancesTool
from agentipy.langchain.helius.mintlists import SolanaHeliusGetMintlistsTool
from agentipy.langchain.helius.nft_events import SolanaHeliusGetNftEventsTool
from agentipy.langchain.helius.nft_fingerprint import \
    SolanaHeliusGetNFTFingerprintTool
from agentipy.langchain.helius.nft_metadata import \
    SolanaHeliusGetNFTMetadataTool
from agentipy.langchain.helius.parsed_transaction_history import \
    SolanaHeliusGetParsedTransactionHistoryTool
from agentipy.langchain.helius.parsed_transactions import \
    SolanaHeliusGetParsedTransactionsTool
from agentipy.langchain.helius.raw_transcations import \
    SolanaHeliusGetRawTransactionsTool
from agentipy.langchain.helius.webhooks import (SolanaHeliusCreateWebhookTool,
                                                SolanaHeliusDeleteWebhookTool,
                                                SolanaHeliusEditWebhookTool,
                                                SolanaHeliusGetAllWebhooksTool,
                                                SolanaHeliusGetWebhookTool)


def get_helius_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaHeliusGetMintlistsTool(solana_kit=solana_kit),
        SolanaHeliusGetActiveListingsTool(solana_kit=solana_kit),
        SolanaHeliusGetAddressNameTool(solana_kit=solana_kit),
        SolanaHeliusGetBalancesTool(solana_kit=solana_kit),
        SolanaHeliusGetNFTFingerprintTool(solana_kit=solana_kit),
        SolanaHeliusGetNFTMetadataTool(solana_kit=solana_kit),
        SolanaHeliusGetNftEventsTool(solana_kit=solana_kit),
        SolanaHeliusGetParsedTransactionHistoryTool(solana_kit=solana_kit),
        SolanaHeliusGetParsedTransactionsTool(solana_kit=solana_kit),
        SolanaHeliusGetRawTransactionsTool(solana_kit=solana_kit),
        SolanaHeliusGetWebhookTool(solana_kit=solana_kit),
        SolanaHeliusCreateWebhookTool(solana_kit=solana_kit),
        SolanaHeliusDeleteWebhookTool(solana_kit=solana_kit),
        SolanaHeliusGetAllWebhooksTool(solana_kit=solana_kit),
        SolanaHeliusEditWebhookTool(solana_kit=solana_kit),
        
    ]
