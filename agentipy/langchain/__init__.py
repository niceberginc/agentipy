from agentipy.agent import SolanaAgentKit
from agentipy.langchain.backpack import get_backpack_tools

from agentipy.langchain.curve import get_curve_tools
from agentipy.langchain.cybersmanager import get_cyber_tools
from agentipy.langchain.drift import get_drift_tools
from agentipy.langchain.faucet import get_faucet_tools
from agentipy.langchain.helius import get_helius_tools
from agentipy.langchain.core import get_all_core_tools
from agentipy.langchain.lightprotocolmanager import get_light_protocol_tools
from agentipy.langchain.lulo import get_lulo_tools
from agentipy.langchain.flash import get_flash_tools
from agentipy.langchain.land3 import get_land_tools
from agentipy.langchain.manifest import get_manifest_tools
from agentipy.langchain.oracle import get_stork_tools
from agentipy.langchain.orca import get_orca_tools
from agentipy.langchain.raydium import get_raydium_tools
from agentipy.langchain.pumpfun import get_pumpfun_tools
from agentipy.langchain.meteora import get_meteora_tools
from agentipy.langchain.moonshot import get_moonshot_tools
from agentipy.langchain.fluxbeam import get_fluxbeam_tools
from agentipy.langchain.gibwork import get_gibwork_tools
from agentipy.langchain.perpetual import get_perp_tools
from agentipy.langchain.domain import get_domain_tools
from agentipy.langchain.sns import get_sns_tools
from agentipy.langchain.coingecko import get_coingecko_tools
from agentipy.langchain.debridge import get_debridge_tools
from agentipy.langchain.metaplex import get_metaplex_tools
from agentipy.langchain.jito import get_jito_tools
from agentipy.langchain.elfaai import get_elfaai_tools

def create_solana_tools(solana_kit: SolanaAgentKit):
    return [
        *get_helius_tools(solana_kit=solana_kit),
        *get_all_core_tools(solana_kit=solana_kit),
        *get_lulo_tools(solana_kit=solana_kit),
        *get_flash_tools(solana_kit=solana_kit),
        *get_land_tools(solana_kit=solana_kit),
        *get_metaplex_tools(solana_kit=solana_kit),
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
      
        *get_cyber_tools(solana_kit=solana_kit),
        *get_faucet_tools(solana_kit=solana_kit),
        *get_curve_tools(solana_kit=solana_kit),
       
        *get_light_protocol_tools(solana_kit=solana_kit),
        *get_stork_tools(solana_kit=solana_kit),
        *get_backpack_tools(solana_kit=solana_kit),
        *get_jito_tools(solana_kit=solana_kit) ,
        *get_elfaai_tools(solana_kit=solana_kit),
        *get_metaplex_tools(solana_kit=solana_kit),
        *get_debridge_tools(solana_kit=solana_kit),
        *get_drift_tools(solana_kit=solana_kit),
        *get_manifest_tools(solana_kit=solana_kit),
        *get_orca_tools(solana_kit=solana_kit),
    ]   

