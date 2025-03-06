from agentipy.agent import SolanaAgentKit
from agentipy.langchain.squads.approve_multisig_proposal import \
    SquadsApproveMultisigProposalTool
from agentipy.langchain.squads.create_multisig import SquadsCreateMultisigTool
from agentipy.langchain.squads.create_multisig_proposal import \
    SquadsCreateMultisigProposalTool
from agentipy.langchain.squads.deposit_to_multisig_treasury import \
    SquadsDepositToMultisigTreasuryTool
from agentipy.langchain.squads.execute_multisig_proposal import \
    SquadsExecuteMultisigProposalTool
from agentipy.langchain.squads.reject_multisig_proposal import \
    SquadsRejectMultisigProposalTool
from agentipy.langchain.squads.transfer_from_multisig import \
    SquadsTransferFromMultisigTreasuryTool


def get_squads_tools(solana_kit: SolanaAgentKit):
    return [
        SquadsApproveMultisigProposalTool(agent_kit=solana_kit),
        SquadsCreateMultisigTool(agent_kit=solana_kit),
        SquadsCreateMultisigProposalTool(agent_kit=solana_kit),
        SquadsDepositToMultisigTreasuryTool(agent_kit=solana_kit),
        SquadsExecuteMultisigProposalTool(agent_kit=solana_kit),
        SquadsTransferFromMultisigTreasuryTool(agent_kit=solana_kit),
        SquadsRejectMultisigProposalTool(agent_kit=solana_kit),
    ]