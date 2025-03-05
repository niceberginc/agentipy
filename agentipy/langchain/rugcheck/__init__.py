from .fetch_all_domains import RugCheckFetchAllDomainsTool
from .fetch_domains_csv import RugCheckFetchDomainsCSVTool
from .lookup_domain import RugCheckLookupDomainTool
from .fetch_domain_records import RugCheckFetchDomainRecordsTool
from .fetch_leaderboard import RugCheckFetchLeaderboardTool
from .fetch_new_tokens import RugCheckFetchNewTokensTool
from .fetch_most_viewed_tokens import RugCheckFetchMostViewedTokensTool
from .fetch_trending_tokens import RugCheckFetchTrendingTokensTool
from .fetch_recently_verified_tokens import RugCheckFetchRecentlyVerifiedTokensTool
from .fetch_token_lp_lockers import RugCheckFetchTokenLPLockersTool
from .fetch_token_flux_lp_lockers import RugCheckFetchTokenFluxLPLockersTool
from .fetch_token_votes import RugCheckFetchTokenVotesTool
from agentipy.agent import SolanaAgentKit


def get_rugcheck_tools(solana_kit: SolanaAgentKit):
    return [
        RugCheckFetchAllDomainsTool(solana_kit),
        RugCheckFetchDomainsCSVTool(solana_kit),
        RugCheckLookupDomainTool(solana_kit),
        RugCheckFetchDomainRecordsTool(solana_kit),
        RugCheckFetchLeaderboardTool(solana_kit),
        RugCheckFetchNewTokensTool(solana_kit),
        RugCheckFetchMostViewedTokensTool(solana_kit),
        RugCheckFetchTrendingTokensTool(solana_kit),
        RugCheckFetchRecentlyVerifiedTokensTool(solana_kit),
        RugCheckFetchTokenLPLockersTool(solana_kit),
        RugCheckFetchTokenFluxLPLockersTool(solana_kit),
        RugCheckFetchTokenVotesTool(solana_kit)
    ]