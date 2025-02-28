import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input


class SolanaSNSResolveTool(BaseTool):
    name: str = "solana_sns_resolve"
    description: str = """
    Resolves a Solana Name Service (SNS) domain to its corresponding address.

    Input: A JSON string with:
    {
        "domain": "string, the SNS domain (e.g., example.sol)"
    }

    Output:
    {
        "address": "string, the resolved Solana address",
        "message": "string, if resolution fails"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "domain": {"type": str, "required": True}
            }
            validate_input(data, schema)

            domain = data["domain"]
            if not domain:
                raise ValueError("Domain is required.")

            address = await self.solana_kit.resolve_name_to_address(domain)
            return {
                "address": address or "Not Found",
                "message": "Success" if address else "Domain not found."
            }
        except Exception as e:
            return {
                "address": None,
                "message": f"Error resolving domain: {str(e)}"
            }

    def _run(self):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

