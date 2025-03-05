from agentipy.agent import SolanaAgentKit
from agentipy.langchain.flash.open_trade import FlashOpenTradeTool
from agentipy.langchain.flash.close_trade import FlashCloseTradeTool


def get_flash_tools(solana_kit: SolanaAgentKit):
    return [
        FlashOpenTradeTool(solana_kit=solana_kit),
        FlashCloseTradeTool(solana_kit=solana_kit)
    ]

            
