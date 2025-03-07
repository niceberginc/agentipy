import json

from langchain.tools import BaseTool

from agentipy.agent.evm import EvmAgentKit
from agentipy.helpers import validate_input


class VirtualsGetSentientListingsTool(BaseTool):
    name: str = "virtuals_get_sentient_listings"
    description: str = """
    Fetches Sentient listings using VirtualsManager.

    Input: A JSON string with:
    {
        "page_number": "int, optional, the page number for pagination (default: 1)",
        "page_size": "int, optional, the number of items per page (default: 30)"
    }
    Output:
    {
        "listings": "dict, the listings data",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "page_number": int,
                "page_size": int
            }
            validate_input(data, schema)

            listings = await self.agent_kit.get_sentient_listings(
                page_number=data.get("page_number", 1),
                page_size=data.get("page_size", 30)
            )
            return {
                "listings": listings,
                "message": "Success"
            }
        except Exception as e:
            return {
                "listings": None,
                "message": f"Error fetching Sentient listings: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsBuySentientTool(BaseTool):
    name: str = "virtuals_buy_sentient"
    description: str = """
    Purchases Sentient tokens using VirtualsManager.

    Input: A JSON string with:
    {
        "token_address": "string, the token address",
        "amount": "string, the amount to purchase",
        "builder_id": "int, optional, the builder ID for the purchase"
    }
    Output:
    {
        "transaction_receipt": "dict, the transaction receipt",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            schema = {
                "token_address": str,
                "amount": str,
                "builder_id": int
            }
            validate_input(data, schema)
            
            transaction_receipt = await self.agent_kit.buy_sentient(
                token_address=data["token_address"],
                amount=data["amount"],
                builder_id=data.get("builder_id")
            )
            return {
                "transaction_receipt": transaction_receipt,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_receipt": None,
                "message": f"Error purchasing Sentient tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsSellSentientTool(BaseTool):
    name: str = "virtuals_sell_sentient"
    description: str = """
    Sells Sentient tokens using VirtualsManager.

    Input: A JSON string with:
    {
        "token_address": "string, the token address",
        "amount": "string, the amount to sell",
        "builder_id": "int, optional, the builder ID for the sale"
    }
    Output:
    {
        "transaction_receipt": "dict, the transaction receipt",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction_receipt = await self.agent_kit.sell_sentient(
                token_address=data["token_address"],
                amount=data["amount"],
                builder_id=data.get("builder_id")
            )
            return {
                "transaction_receipt": transaction_receipt,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_receipt": None,
                "message": f"Error selling Sentient tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsBuyPrototypeTool(BaseTool):
    name: str = "virtuals_buy_prototype"
    description: str = """
    Purchases Prototype tokens using VirtualsManager.

    Input: A JSON string with:
    {
        "token_address": "string, the token address",
        "amount": "string, the amount to purchase",
        "builder_id": "int, optional, the builder ID for the purchase",
        "slippage": "float, optional, the slippage tolerance percentage"
    }
    Output:
    {
        "transaction_receipt": "dict, the transaction receipt",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction_receipt = await self.agent_kit.buy_prototype(
                token_address=data["token_address"],
                amount=data["amount"],
                builder_id=data.get("builder_id"),
                slippage=data.get("slippage")
            )
            return {
                "transaction_receipt": transaction_receipt,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_receipt": None,
                "message": f"Error purchasing Prototype tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsSellPrototypeTool(BaseTool):
    name: str = "virtuals_sell_prototype"
    description: str = """
    Sells Prototype tokens using VirtualsManager.

    Input: A JSON string with:
    {
        "token_address": "string, the token address",
        "amount": "string, the amount to sell",
        "builder_id": "int, optional, the builder ID for the sale",
        "slippage": "float, optional, the slippage tolerance percentage"
    }
    Output:
    {
        "transaction_receipt": "dict, the transaction receipt",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction_receipt = await self.agent_kit.sell_prototype(
                token_address=data["token_address"],
                amount=data["amount"],
                builder_id=data.get("builder_id"),
                slippage=data.get("slippage")
            )
            return {
                "transaction_receipt": transaction_receipt,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_receipt": None,
                "message": f"Error selling Prototype tokens: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsCheckSentientAllowanceTool(BaseTool):
    name: str = "virtuals_check_sentient_allowance"
    description: str = """
    Checks Sentient token allowance using VirtualsManager.

    Input: A JSON string with:
    {
        "amount": "string, the amount to check allowance for",
        "from_token_address": "string, optional, the token address being checked"
    }
    Output:
    {
        "allowance_sufficient": "bool, whether the allowance is sufficient",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            allowance_sufficient = await self.agent_kit.check_sentient_allowance(
                amount=data["amount"],
                from_token_address=data.get("from_token_address")
            )
            return {
                "allowance_sufficient": allowance_sufficient,
                "message": "Success"
            }
        except Exception as e:
            return {
                "allowance_sufficient": None,
                "message": f"Error checking Sentient allowance: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsApproveSentientAllowanceTool(BaseTool):
    name: str = "virtuals_approve_sentient_allowance"
    description: str = """
    Approves Sentient token allowance using VirtualsManager.

    Input: A JSON string with:
    {
        "amount": "string, the amount to approve",
        "from_token_address": "string, optional, the token address being approved"
    }
    Output:
    {
        "transaction_hash": "dict, the transaction hash",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction_hash = await self.agent_kit.approve_sentient_allowance(
                amount=data["amount"],
                from_token_address=data.get("from_token_address")
            )
            return {
                "transaction_hash": transaction_hash,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_hash": None,
                "message": f"Error approving Sentient allowance: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsCheckPrototypeAllowanceTool(BaseTool):
    name: str = "virtuals_check_prototype_allowance"
    description: str = """
    Checks Prototype token allowance using VirtualsManager.

    Input: A JSON string with:
    {
        "amount": "string, the amount to check allowance for",
        "from_token_address": "string, optional, the token address being checked"
    }
    Output:
    {
        "allowance_sufficient": "bool, whether the allowance is sufficient",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            allowance_sufficient = await self.agent_kit.check_prototype_allowance(
                amount=data["amount"],
                from_token_address=data.get("from_token_address")
            )
            return {
                "allowance_sufficient": allowance_sufficient,
                "message": "Success"
            }
        except Exception as e:
            return {
                "allowance_sufficient": None,
                "message": f"Error checking Prototype allowance: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsApprovePrototypeAllowanceTool(BaseTool):
    name: str = "virtuals_approve_prototype_allowance"
    description: str = """
    Approves Prototype token allowance using VirtualsManager.

    Input: A JSON string with:
    {
        "amount": "string, the amount to approve",
        "from_token_address": "string, optional, the token address being approved"
    }
    Output:
    {
        "transaction_hash": "dict, the transaction hash",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            transaction_hash = await self.agent_kit.approve_prototype_allowance(
                amount=data["amount"],
                from_token_address=data.get("from_token_address")
            )
            return {
                "transaction_hash": transaction_hash,
                "message": "Success"
            }
        except Exception as e:
            return {
                "transaction_hash": None,
                "message": f"Error approving Prototype allowance: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsGetPrototypeListingTool(BaseTool):
    name: str = "virtuals_get_prototype_listing"
    description: str = """
    Retrieves Prototype token listings using VirtualsManager.

    Input: A JSON string with:
    {
        "page_number": "int, optional, the page number for pagination (default: 1)",
        "page_size": "int, optional, the number of items per page (default: 30)"
    }
    Output:
    {
        "listings": "dict, the Prototype token listings",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            listings = await self.agent_kit.get_prototype_listing(
                page_number=data.get("page_number", 1),
                page_size=data.get("page_size", 30)
            )
            return {
                "listings": listings,
                "message": "Success"
            }
        except Exception as e:
            return {
                "listings": None,
                "message": f"Error fetching Prototype listings: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsFetchKlinesTool(BaseTool):
    name: str = "virtuals_fetch_klines"
    description: str = """
    Fetches Klines (candlestick chart data) for a token using VirtualsManager.

    Input: A JSON string with:
    {
        "token_address": "string, the token address",
        "granularity": "int, the granularity of the data",
        "start": "int, the start timestamp",
        "end": "int, the end timestamp",
        "limit": "int, the number of data points"
    }
    Output:
    {
        "kline_data": "dict, the Kline data",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            kline_data = await self.agent_kit.fetch_klines(
                token_address=data["token_address"],
                granularity=data["granularity"],
                start=data["start"],
                end=data["end"],
                limit=data["limit"]
            )
            return {
                "kline_data": kline_data,
                "message": "Success"
            }
        except Exception as e:
            return {
                "kline_data": None,
                "message": f"Error fetching Klines: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")

class VirtualsSearchTokenByKeywordTool(BaseTool):
    name: str = "virtuals_search_token_by_keyword"
    description: str = """
    Searches for a virtual token by keyword using VirtualsManager.

    Input: A JSON string with:
    {
        "keyword": "string, the search keyword"
    }
    Output:
    {
        "token_details": "dict, the details of the found token",
        "message": "string, if an error occurs"
    }
    """
    agent_kit: EvmAgentKit

    async def _arun(self, input: str):
        try:
            data = json.loads(input)
            token_details = await self.agent_kit.search_virtual_token_by_keyword(
                keyword=data["keyword"]
            )
            return {
                "token_details": token_details,
                "message": "Success"
            }
        except Exception as e:
            return {
                "token_details": None,
                "message": f"Error searching virtual token by keyword: {str(e)}"
            }

    def _run(self, input: str):
        raise NotImplementedError("This tool only supports async execution via _arun. Please use the async interface.")


def create_evm_tools(evm_kit: EvmAgentKit):
    return [
        VirtualsGetSentientListingsTool(agent_kit=evm_kit),
        VirtualsBuySentientTool(agent_kit=evm_kit),
        VirtualsSellSentientTool(agent_kit=evm_kit),
        VirtualsBuyPrototypeTool(agent_kit=evm_kit),
        VirtualsSellPrototypeTool(agent_kit=evm_kit),
        VirtualsCheckSentientAllowanceTool(agent_kit=evm_kit),
        VirtualsApproveSentientAllowanceTool(agent_kit=evm_kit),
        VirtualsCheckPrototypeAllowanceTool(agent_kit=evm_kit),
        VirtualsApprovePrototypeAllowanceTool(agent_kit=evm_kit),
        VirtualsGetPrototypeListingTool(agent_kit=evm_kit),
        VirtualsFetchKlinesTool(agent_kit=evm_kit),
        VirtualsSearchTokenByKeywordTool(agent_kit=evm_kit)
    ]