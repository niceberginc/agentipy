from agentipy.agent import SolanaAgentKit
from agentipy.langchain.domain.all_domains import ResolveAllDomainsTool
from agentipy.langchain.domain.owned_domains import GetOwnedDomainsForTLDTool
from agentipy.langchain.domain.all_top_level_domain import GetAllDomainsTLDsTool
from agentipy.langchain.domain.get_all_domain import GetOwnedAllDomainsTool


def get_domain_tools(solana_kit: SolanaAgentKit):
    return [
        ResolveAllDomainsTool(solana_kit=solana_kit),
        GetOwnedDomainsForTLDTool(solana_kit=solana_kit),
        GetAllDomainsTLDsTool(solana_kit=solana_kit),
        GetOwnedAllDomainsTool(solana_kit=solana_kit)
    ]
