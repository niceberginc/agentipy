import json
from typing import Optional

from langchain.tools import BaseTool

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class RentShieldCheckTokenTool(BaseTool):
    name: str = "rentshield_check_token"
    description: str = """
    Runs a read-only 11-layer pre-buy rug and scam audit on a Solana token mint via Rent & Rug Shield.

    Input: A JSON string with:
    {
        "mint": "string, public base58 Solana token mint address (never pass private keys)"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str) -> str:
        try:
            data = json.loads(input) if input.strip().startswith("{") else {"mint": input.strip()}
            validate_input(data, {"mint": {"type": str, "required": True}})
            report = await self.agent_kit.check_token_rug_shield(data["mint"])
            return json.dumps({"status": "success", "report": report})
        except Exception as exc:
            return json.dumps({"status": "error", "message": str(exc)})

    def _run(self, input: Optional[str] = None) -> str:
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )


class RentShieldScanWalletTool(BaseTool):
    name: str = "rentshield_scan_wallet_rent"
    description: str = """
    Read-only, non-custodial scan for reclaimable SOL rent locked in empty SPL and Token-2022 token accounts (0% fee on first claim).

    Input: Optional JSON string with:
    {
        "wallet": "string, optional public base58 Solana wallet address (defaults to agent public wallet_address)"
    }
    """
    agent_kit: SolanaAgentKit

    async def _arun(self, input: str = "") -> str:
        try:
            wallet: Optional[str] = None
            stripped = (input or "").strip()
            if stripped:
                data = json.loads(stripped) if stripped.startswith("{") else {"wallet": stripped}
                wallet = data.get("wallet")
            result = await self.agent_kit.scan_wallet_unclaimed_rent(wallet)
            return json.dumps({"status": "success", "result": result})
        except Exception as exc:
            return json.dumps({"status": "error", "message": str(exc)})

    def _run(self, input: Optional[str] = None) -> str:
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )
