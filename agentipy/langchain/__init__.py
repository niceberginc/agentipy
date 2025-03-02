from agentipy.langchain.backpack import get_backpack_tools
from agentipy.langchain.buy_and_sell_tools import get_buy_and_sell_tools
from agentipy.langchain.curve_tools import get_curve_tools
from agentipy.langchain.cyber import get_cyber_tools
from agentipy.langchain.faucet import get_faucet_tools
from agentipy.langchain.helius import get_helius_tools
from agentipy.langchain.core import get_all_core_tools
from agentipy.langchain.light_protocol import get_light_protocol_tools
from agentipy.langchain.lulo_tools import get_lulo_tools
from agentipy.langchain.flash_tools import get_flash_tools
from agentipy.langchain.land_tools import get_land_tools
from agentipy.langchain.oracle import get_stork_tools
from agentipy.langchain.raydium_tools import get_raydium_tools
from agentipy.langchain.pumpfun_tools import get_pumpfun_tools
from agentipy.langchain.meterora_tools import get_meteora_tools
from agentipy.langchain.moonshot_tools import get_moonshot_tools
from agentipy.langchain.fluxbeam_tools import get_fluxbeam_tools
from agentipy.langchain.gibwork_tools import get_gibwork_tools
from agentipy.langchain.perp import get_perp_tools
from agentipy.langchain.domain_tools import get_domain_tools
from agentipy.langchain.sns import get_sns_tools
from agentipy.langchain.coingecko import get_coingecko_tools
from agentipy.langchain.debridge import get_debridge_tools
from agentipy.langchain.burn_tools import get_burn_tools



def create_solana_tools(solana_kit: SolanaAgentKit):
    return [
        *get_helius_tools(solana_kit=solana_kit),
        *get_all_core_tools(solana_kit=solana_kit),
        *get_lulo_tools(solana_kit=solana_kit),
        *get_flash_tools(solana_kit=solana_kit),
        *get_land_tools(solana_kit=solana_kit),
        *get_burn_tools(solana_kit=solana_kit),
        *get_raydium_tools(solana_kit=solana_kit),
        *get_pumpfun_tools(solana_kit=solana_kit),
        *get_meteora_tools(solana_kit=solana_kit),
        *get_moonshot_tools(solana_kit=solana_kit),
        *get_fluxbeam_tools(solana_kit=solana_kit),
        *get_gibwork_tools(solana_kit=solana_kit),
        *get_perp_tools(solana_kit=solana_kit),
        *get_domain_tools(solana_kit=solana_kit),
        *get_sns_tools(solana_kit=solana_kit),
        *get_coingecko_tools(solana_kit=solana_kit),
        *get_debridge_tools(solana_kit=solana_kit),
        *get_burn_tools(solana_kit=solana_kit),
        *get_cyber_tools(solana_kit=solana_kit),
        *get_faucet_tools(solana_kit=solana_kit),
        *get_curve_tools(solana_kit=solana_kit),
        *get_buy_and_sell_tools(solana_kit=solana_kit),
        *get_light_protocol_tools(solana_kit=solana_kit),
        *get_stork_tools(solana_kit=solana_kit),
        *get_backpack_tools(solana_kit=solana_kit)  
    ]   

