from agentipy.agent import SolanaAgentKit
from agentipy.langchain.perpetual.close_perp_trade_short import ClosePerpTradeShortTool
from agentipy.langchain.perpetual.close_perp_trade_long import ClosePerpTradeLongTool
from agentipy.langchain.perpetual.open_perp_trade_long import OpenPerpTradeLongTool
from agentipy.langchain.perpetual.open_perp_trade_short import OpenPerpTradeShortTool


def get_perp_tools(solana_kit: SolanaAgentKit):
    return [
        ClosePerpTradeShortTool(solana_kit=solana_kit),
        ClosePerpTradeLongTool(solana_kit=solana_kit),
        OpenPerpTradeLongTool(solana_kit=solana_kit),
        OpenPerpTradeShortTool(solana_kit=solana_kit)
    ]

