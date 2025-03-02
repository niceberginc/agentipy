import json
from langchain.tools import BaseTool
from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input



class SolanaGetMetaplexAssetsByCreatorTool(BaseTool):
    name: str = "solana_get_metaplex_assets_by_creator"
    description: str = """
    Fetches assets created by a specific creator.

    Input: A JSON string with:
    {
        "creator": "string, the creator's public key",
        "only_verified": "bool, fetch only verified assets (default: False)",
        "sort_by": "string, field to sort by (e.g., 'date')",
        "sort_direction": "string, 'asc' or 'desc'",
        "limit": "int, maximum number of assets",
        "page": "int, page number for paginated results"
    }

    Output:
    {
        "success": "bool, whether the operation was successful",
        "value": "list, the list of assets if successful",
        "message": "string, additional details or error information"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "creator": {"type": str, "required": True},
                "only_verified": {"type": bool, "required": False},
                "sort_by": {"type": str, "required": False},
                "sort_direction": {"type": str, "required": False},
                "limit": {"type": int, "required": False, "min": 1},
                "page": {"type": int, "required": False, "min": 1}
            }
            validate_input(data, schema)

            creator = data["creator"]
            only_verified = data.get("only_verified", False)
            sort_by = data.get("sort_by")
            sort_direction = data.get("sort_direction")
            limit = data.get("limit")
            page = data.get("page")

            result = await self.solana_kit.get_metaplex_assets_by_creator(
                creator=creator,
                onlyVerified=only_verified,
                sortBy=sort_by,
                sortDirection=sort_direction,
                limit=limit,
                page=page,
            )
            return result
        except Exception as e:
            return {"success": False, "message": f"Error fetching assets by creator: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class SolanaGetMetaplexAssetsByAuthorityTool(BaseTool):
    name: str = "solana_get_metaplex_assets_by_authority"
    description: str = """
    Fetches assets created by a specific authority.

    Input: A JSON string with:
    {
        "authority": "string, the authority's public key",
        "sort_by": "string, field to sort by (e.g., 'date')",
        "sort_direction": "string, 'asc' or 'desc'",
        "limit": "int, maximum number of assets",
        "page": "int, page number for paginated results"
    }

    Output:
    {
        "success": "bool, whether the operation was successful",
        "value": "list, the list of assets if successful",
        "message": "string, additional details or error information"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "authority": {"type": str, "required": True},
                "sort_by": {"type": str, "required": False},
                "sort_direction": {"type": str, "required": False},
                "limit": {"type": int, "required": False, "min": 1},
                "page": {"type": int, "required": False, "min": 1}
            }
            validate_input(data, schema)

            authority = data["authority"]
            sort_by = data.get("sort_by")
            sort_direction = data.get("sort_direction")
            limit = data.get("limit")
            page = data.get("page")

            result = await self.solana_kit.get_metaplex_assets_by_authority(
                authority=authority,
                sortBy=sort_by,
                sortDirection=sort_direction,
                limit=limit,
                page=page,
            )
            return result
        except Exception as e:
            return {"success": False, "message": f"Error fetching assets by authority: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class SolanaDeployCollectionTool(BaseTool):
    name: str = "solana_deploy_collection"
    description: str = """
    Deploys an NFT collection using the Metaplex program.

    Input: A JSON string with:
    {
        "name": "string, the name of the NFT collection",
        "uri": "string, the metadata URI",
        "royalty_basis_points": "int, royalty percentage in basis points (e.g., 500 for 5%)",
        "creator_address": "string, the creator's public key"
    }

    Output:
    {
        "success": "bool, whether the operation was successful",
        "value": "string, the transaction signature if successful",
        "message": "string, additional details or error information"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "name": {"type": str, "required": True},
                "uri": {"type": str, "required": True},
                "royalty_basis_points": {"type": int, "required": True, "min": 0, "max": 10000},
                "creator_address": {"type": str, "required": True}
            }
            validate_input(data, schema)

            name = data["name"]
            uri = data["uri"]
            royalty_basis_points = data["royalty_basis_points"]
            creator_address = data["creator_address"]

            result = await self.solana_kit.deploy_collection(
                name=name,
                uri=uri,
                royalty_basis_points=royalty_basis_points,
                creator_address=creator_address,
            )
            return result
        except Exception as e:
            return {"success": False, "message": f"Error deploying collection: {str(e)}"}

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
