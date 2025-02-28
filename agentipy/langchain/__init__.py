import json

from langchain.tools import BaseTool
from solders.pubkey import Pubkey  # type: ignore

from agentipy.agent import SolanaAgentKit
from agentipy.helpers import validate_input
from agentipy.langchain.backpack_tools import get_backpack_tools
from agentipy.langchain.burn_tools import get_burn_tools
from agentipy.langchain.driftvault_tools import get_driftvault_tools
from agentipy.langchain.elfaai_tools import get_elfaai_tools
from agentipy.langchain.flash_tools import get_flash_tools
from agentipy.langchain.fluxbeam_tools import get_fluxbeam_tools
from agentipy.langchain.gibwork_tools import get_gibwork_tools
from agentipy.langchain.helius_tools import get_helius_tools
from agentipy.langchain.land_tools import get_land_tools
from agentipy.langchain.lulo_tools import get_lulo_tools
from agentipy.langchain.manifest_tools import get_manifest_tools
from agentipy.langchain.metaplex_tools import get_metaplex_tools
from agentipy.langchain.meterora_tools import get_meteora_tools
from agentipy.langchain.moonshot_tools import SolanaBuyUsingMoonshotTool, SolanaSellUsingMoonshotTool, get_moonshot_tools
from agentipy.langchain.orca_tools import get_orca_tools
from agentipy.langchain.perp_tools import get_perp_tools
from agentipy.langchain.pumpfun_tools import get_pumpfun_tools
from agentipy.langchain.raydium_tools import SolanaRaydiumBuyTool, SolanaRaydiumSellTool, get_raydium_tools
from agentipy.langchain.sns_tools import get_sns_tools



 





  



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



class SolanaCybersCreateCoinTool(BaseTool):
    name: str = "cybers_create_coin"
    description: str = """
    Creates a new coin using the CybersManager.

    Input: A JSON string with:
    {
        "name": "string, the name of the coin",
        "symbol": "string, the symbol of the coin",
        "image_path": "string, the file path to the coin's image",
        "tweet_author_id": "string, the Twitter ID of the coin's author",
        "tweet_author_username": "string, the Twitter username of the coin's author"
    }

    Output:
    {
        "coin_id": "string, the unique ID of the created coin",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "name": {"type": str, "required": True},
                "symbol": {"type": str, "required": True},
                "image_path": {"type": str, "required": True},
                "tweet_author_id": {"type": str, "required": True},
                "tweet_author_username": {"type": str, "required": True}
            }
            validate_input(data, schema)

            name = data["name"]
            symbol = data["symbol"]
            image_path = data["image_path"]
            tweet_author_id = data["tweet_author_id"]
            tweet_author_username = data["tweet_author_username"]

            coin_id = await self.solana_kit.cybers_create_coin(
                name=name,
                symbol=symbol,
                image_path=image_path,
                tweet_author_id=tweet_author_id,
                tweet_author_username=tweet_author_username
            )
            return {
                "coin_id": coin_id,
                "message": "Success"
            }
        except Exception as e:
            return {
                "coin_id": None,
                "message": f"Error creating coin: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaGetTipAccounts(BaseTool):
    name: str = "get_tip_accounts"
    description: str = """
    Get all available Jito tip accounts.

    Output:
    {
        "accounts": "List of Jito tip accounts"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            result = await self.solana_kit.get_tip_accounts()
            return {
                "accounts": result
            }
        except Exception as e:
            return {
                "accounts": None
            }

    def _run(self, input: str):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )

class SolanaGetRandomTipAccount(BaseTool):
    name: str = "get_random_tip_account"
    description: str = """
    Get a randomly selected Jito tip account from the existing list.

    Output:
    {
        "account": "Randomly selected Jito tip account"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self):
        try:
            result = await self.solana_kit.get_random_tip_account()
            return {
                "account": result
            }
        except Exception as e:
            return {
                "account": None
            }

    def _run(self):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )


class SolanaSendTxn(BaseTool):
    name: str = "send_txn"
    description: str = """
    Send an individual transaction to the Jito network for processing.

    Input: A JSON string with:
    {
        "txn_signature": "string, the transaction signature",
        "bundleOnly": "boolean, whether to send the transaction as a bundle"
    }

    Output:
    {
        "status": "Unique identifier of the processed transaction bundle"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "txn_signature": {"type": str, "required": True},
                "bundleOnly": {"type": bool, "required": True}
            }
            validate_input(data, schema)

            txn_signature = data["txn_signature"]
            bundleOnly = data["bundleOnly"]
            result = await self.solana_kit.send_txn(txn_signature, bundleOnly)
            return {
                "status": result
            }
        except Exception as e:
            return {
                "status": None
            }

    def _run(self):
        raise NotImplementedError(
            "This tool only supports async execution via _arun. Please use the async interface."
        )


class StorkGetPriceTool(BaseTool):
    name: str = "stork_get_price"
    description: str = """
    Fetch the price of an asset using the Stork Oracle.

    Input: A JSON string with:
    {
        "asset_id": "string, the asset pair ID to fetch price data for (e.g., SOLUSD)."
    }

    Output:
    {
        "price": float, # the token price,
        "timestamp": int, # the unix nanosecond timestamp of the price
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            asset_id = data["asset_id"]
            
            result = await self.solana_kit.stork_fetch_price(asset_id)
            return {
                "status": "success",
                "data": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")
    

   

  
class LightProtocolSendCompressedAirdropTool(BaseTool):
    name: str = "lightprotocol_send_compressed_airdrop"
    description: str = """
    Sends a compressed airdrop using LightProtocolManager.

    Input: A JSON string with:
    {
        "mint_address": "string, the mint address of the token",
        "amount": "float, the amount to send",
        "decimals": "int, the number of decimal places for the token",
        "recipients": "list, the list of recipient addresses",
        "priority_fee_in_lamports": "int, the priority fee in lamports",
        "should_log": "bool, optional, whether to log the transaction"
    }
    Output:
    {
        "transaction_ids": "list, transaction IDs of the airdrop",
        "message": "string, if an error occurs"
    }
    """
    solana_kit: SolanaAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "mint_address": {"type": str, "required": True},
                "amount": {"type": float, "required": True},
                "decimals": {"type": int, "required": True},
                "recipients": {"type": list, "required": True},
                "priority_fee_in_lamports": {"type": int, "required": True},
                "should_log": {"type": bool, "required": False}
            }
            validate_input(data, schema)
            
            transaction_ids = await self.solana_kit.send_compressed_airdrop(
                mint_address=data["mint_address"],
                amount=data["amount"],
                decimals=data["decimals"],
                recipients=data["recipients"],
                priority_fee_in_lamports=data["priority_fee_in_lamports"],
                should_log=data.get("should_log", False)
            )
            return {
                "transaction_ids": transaction_ids,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_ids": None,
                "message": f"Error sending compressed airdrop: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")






def create_solana_tools(solana_kit: SolanaAgentKit):
    return [
     get_backpack_tools(solana_kit=solana_kit),
     get_driftvault_tools(solana_kit=solana_kit),
     get_elfaai_tools(solana_kit=solana_kit),
     get_flash_tools(solana_kit=solana_kit),
     get_fluxbeam_tools(solana_kit=solana_kit),
     get_gibwork_tools(solana_kit=solana_kit),
     get_helius_tools(solana_kit=solana_kit),
     get_land_tools(solana_kit=solana_kit),
     get_lulo_tools(solana_kit=solana_kit),
     get_manifest_tools(solana_kit=solana_kit),
     get_metaplex_tools(solana_kit=solana_kit),
     get_meteora_tools(solana_kit=solana_kit),
     get_moonshot_tools(solana_kit=solana_kit),
     get_orca_tools(solana_kit=solana_kit),
     get_perp_tools(solana_kit=solana_kit),
     get_pumpfun_tools(solana_kit=solana_kit),
     get_raydium_tools(solana_kit=solana_kit),
     get_sns_tools(solana_kit=solana_kit),
     get_burn_tools(solana_kit=solana_kit),
     

        SolanaRaydiumBuyTool(solana_kit=solana_kit),
        SolanaRaydiumSellTool(solana_kit=solana_kit),
        SolanaCreateGibworkTaskTool(solana_kit=solana_kit),
        SolanaSellUsingMoonshotTool(solana_kit=solana_kit),
        SolanaBuyUsingMoonshotTool(solana_kit=solana_kit),
       
       
        LightProtocolSendCompressedAirdropTool(solana_kit=solana_kit),
        
    ]

