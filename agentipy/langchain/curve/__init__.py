from agentipy.agent import SolanaAgentKit
from agentipy.langchain.curve.pump_curve_state import SolanaGetPumpCurveStateTool
from agentipy.langchain.curve.calculate_pump_curve import SolanaCalculatePumpCurvePriceTool


def get_curve_tools(solana_kit: SolanaAgentKit):
    return [
        SolanaGetPumpCurveStateTool(solana_kit=solana_kit),
        SolanaCalculatePumpCurvePriceTool(solana_kit=solana_kit),
    ]