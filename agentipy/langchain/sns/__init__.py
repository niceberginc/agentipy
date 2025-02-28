from agentipy.agent import SolanaAgentKit
from agentipy.langchain.sns.all_domains import SolanaSNSGetAllDomainsTool
from agentipy.langchain.sns.favourite_domain import SolanaSNSGetFavouriteDomainTool
from agentipy.langchain.sns.register import SolanaSNSRegisterDomainTool
from agentipy.langchain.sns.resolve import SolanaSNSResolveTool

def get_sns_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaSNSGetAllDomainsTool(solana_kit=solana_kit),
        SolanaSNSGetFavouriteDomainTool(solana_kit=solana_kit),
        SolanaSNSRegisterDomainTool(solana_kit=solana_kit),
        SolanaSNSResolveTool(solana_kit=solana_kit)
    ]
