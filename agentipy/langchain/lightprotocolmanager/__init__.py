from agentipy.agent import SolanaAgentKit
from agentipy.langchain.lightprotocolmanager.send import LightProtocolSendCompressedAirdropTool


def get_light_protocol_tools(solana_kit: SolanaAgentKit):
    return [
        LightProtocolSendCompressedAirdropTool(solana_kit=solana_kit),
    ]