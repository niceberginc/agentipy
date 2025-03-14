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
        ElfaAiPingApiTool(agent_kit=solana_kit),  
        ElfaAiGetApiKeyStatusTool(agent_kit=solana_kit),
        ElfaAiGetSmartMentionsTool(agent_kit=solana_kit),  
        ElfaAiGetTopMentionsByTickerTool(agent_kit=solana_kit),
        ElfaAiSearchMentionsByKeywordsTool(agent_kit=solana_kit),
        ElfaAiGetTrendingTokensTool(agent_kit=solana_kit),  
        ElfaAiGetSmartTwitterAccountStatsTool(agent_kit=solana_kit) 
    ]