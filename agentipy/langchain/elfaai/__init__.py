from agentipy.agent import SolanaAgentKit
from agentipy.langchain.elfaai.api import (
    ElfaAiPingApiTool,
    ElfaAiGetApiKeyStatusTool
)
from agentipy.langchain.elfaai.mentions import (
    ElfaAiGetSmartMentionsTool,
    ElfaAiGetTopMentionsByTickerTool,
    ElfaAiSearchMentionsByKeywordsTool
)
from agentipy.langchain.elfaai.tokens import ElfaAiGetTrendingTokensTool
from agentipy.langchain.elfaai.twitter import ElfaAiGetSmartTwitterAccountStatsTool


def get_elfaai_tools(solana_kit: SolanaAgentKit):
    return [
        ElfaAiPingApiTool(solana_kit=solana_kit),
        ElfaAiGetApiKeyStatusTool(solana_kit=solana_kit),
        ElfaAiGetSmartMentionsTool(solana_kit=solana_kit),
        ElfaAiGetTopMentionsByTickerTool(solana_kit=solana_kit),
        ElfaAiSearchMentionsByKeywordsTool(solana_kit=solana_kit),
        ElfaAiGetTrendingTokensTool(solana_kit=solana_kit),
        ElfaAiGetSmartTwitterAccountStatsTool(solana_kit=solana_kit)
    ]
