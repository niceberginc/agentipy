import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaSNSRegisterDomainTool(BaseTool):
    name: str = "solana_sns_register_domain"
    description: str = """
    Prepares a transaction to register a new SNS domain.

    Input: A JSON string with:
    {
        "domain": "string, the domain to register",
        "buyer": "string, base58 public key of the buyer's wallet",
        "buyer_token_account": "string, base58 public key of the buyer's token account",
        "space": "integer, bytes to allocate for the domain",
        "mint": "string, optional, the token mint public key (default: USDC)",
        "referrer_key": "string, optional, base58 public key of the referrer"
    }

    Output:
    {
        "transaction": "string, base64-encoded transaction object",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "domain": {"type": str, "required": True},
                "buyer": {"type": str, "required": True},
                "buyer_token_account": {"type": str, "required": True},
                "space": {"type": int, "required": True, "min": 1},
                "mint": {"type": str, "required": False},
                "referrer_key": {"type": str, "required": False}
            }
            validate_input(data, schema)

            domain = data["domain"]
            buyer = data["buyer"]
            buyer_token_account = data["buyer_token_account"]
            space = data["space"]
            mint = data.get("mint")
            referrer_key = data.get("referrer_key")

            transaction = await self.solana_kit.get_registration_transaction(
                domain, buyer, buyer_token_account, space, mint, referrer_key
            )
            return {
                "transaction": transaction,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction": None,
                "message": f"Error preparing registration transaction: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

