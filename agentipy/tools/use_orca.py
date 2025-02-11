import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent import SolanaAgentKit
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)

class OrcaManager:
    @staticmethod
    def close_position(
        agent: SolanaAgentKit,
        position_mint_address: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Closes a position on Orca.

        :param agent: An instance of SolanaAgentKit.
        :param position_mint_address: The mint address of the position to close.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not position_mint_address:
                raise ValueError("Position mint address is required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "positionMintAddress": position_mint_address,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/orca-close-position",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Orca position closing: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Orca position closing: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def create_clmm(
        agent: SolanaAgentKit,
        mint_deploy: str,
        mint_pair: str,
        initial_price: float,
        fee_tier: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a CLMM (Concentrated Liquidity Market Maker) on Orca.

        :param agent: An instance of SolanaAgentKit.
        :param mint_deploy: Base token mint address.
        :param mint_pair: Quote token mint address.
        :param initial_price: Initial price.
        :param fee_tier: Fee tier.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not all([mint_deploy, mint_pair, initial_price, fee_tier]):
                raise ValueError("Mint deploy, mint pair, initial price, and fee tier are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "mintDeploy": mint_deploy,
                "mintPair": mint_pair,
                "initialPrice": initial_price,
                "feeTier": fee_tier,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/orca-create-clmm",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Orca CLMM creation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Orca CLMM creation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def create_liquidity_pool(
        agent: SolanaAgentKit,
        deposit_token_amount: float,
        deposit_token_mint: str,
        other_token_mint: str,
        initial_price: float,
        max_price: float,
        fee_tier: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Creates a single-sided liquidity pool on Orca.

        :param agent: An instance of SolanaAgentKit.
        :param deposit_token_amount: Amount of deposit token.
        :param deposit_token_mint: Mint address of the deposit token.
        :param other_token_mint: Mint address of the other token.
        :param initial_price: Initial price of the pool.
        :param max_price: Maximum price range for the pool.
        :param fee_tier: Fee tier.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not all([deposit_token_amount, deposit_token_mint, other_token_mint, initial_price, max_price, fee_tier]):
                raise ValueError("All parameters are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "depositTokenAmount": deposit_token_amount,
                "depositTokenMint": deposit_token_mint,
                "otherTokenMint": other_token_mint,
                "initialPrice": initial_price,
                "maxPrice": max_price,
                "feeTier": fee_tier,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/orca-create-liquidity-pool",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "transaction": data.get("value"),
                    "message": data.get("message"),
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during Orca liquidity pool creation: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except ValueError as value_error:
            logger.error(f"Validation error: {value_error}", exc_info=True)
            return {"success": False, "error": str(value_error)}
        except Exception as error:
            logger.error(f"Unexpected error during Orca liquidity pool creation: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def fetch_positions(agent: SolanaAgentKit) -> Optional[Dict[str, Any]]:
        """
        Fetches all open positions for the user's Orca account.

        :param agent: An instance of SolanaAgentKit.
        :return: A dictionary containing open positions or error details.
        """
        try:
            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/orca-fetch-positions",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "positions": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during fetching Orca positions: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during fetching Orca positions: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def open_centered_position(
        agent: SolanaAgentKit,
        whirlpool_address: str,
        price_offset_bps: int,
        input_token_mint: str,
        input_amount: float,
    ) -> Optional[Dict[str, Any]]:
        """
        Opens a centered position with liquidity on Orca.

        :param agent: An instance of SolanaAgentKit.
        :param whirlpool_address: Address of the liquidity pool.
        :param price_offset_bps: Basis points offset from current price.
        :param input_token_mint: Mint address of the token used for liquidity.
        :param input_amount: Amount of input token.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not all([whirlpool_address, price_offset_bps, input_token_mint, input_amount]):
                raise ValueError("All parameters are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "whirlpoolAddress": whirlpool_address,
                "priceOffsetBps": price_offset_bps,
                "inputTokenMint": input_token_mint,
                "inputAmount": input_amount,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/orca-open-centered-position",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "transaction": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during opening centered position: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during opening centered position: {error}", exc_info=True)
            return {"success": False, "error": str(error)}

    @staticmethod
    def open_single_sided_position(
        agent: SolanaAgentKit,
        whirlpool_address: str,
        distance_from_current_price_bps: int,
        width_bps: int,
        input_token_mint: str,
        input_amount: float,
    ) -> Optional[Dict[str, Any]]:
        """
        Opens a single-sided liquidity position on Orca.

        :param agent: An instance of SolanaAgentKit.
        :param whirlpool_address: Address of the liquidity pool.
        :param distance_from_current_price_bps: Distance in basis points from the current price.
        :param width_bps: Width in basis points.
        :param input_token_mint: Mint address of the input token.
        :param input_amount: Amount of input token.
        :return: A dictionary containing the transaction signature or error details.
        """
        try:
            if not all([whirlpool_address, distance_from_current_price_bps, width_bps, input_token_mint, input_amount]):
                raise ValueError("All parameters are required.")

            encrypted_private_key = encrypt_private_key(agent.private_key)

            payload: Dict[str, Any] = {
                "requestId": encrypted_private_key["requestId"],
                "encrypted_private_key": encrypted_private_key["encryptedPrivateKey"],
                "rpc_url": agent.rpc_url,
                "open_api_key": agent.openai_api_key,
                "whirlpoolAddress": whirlpool_address,
                "distanceFromCurrentPriceBps": distance_from_current_price_bps,
                "widthBps": width_bps,
                "inputTokenMint": input_token_mint,
                "inputAmount": input_amount,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/orca-open-single-sided-position",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {"success": True, "transaction": data.get("value"), "message": data.get("message")}
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(f"HTTP error during opening single-sided position: {http_error}", exc_info=True)
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(f"Unexpected error during opening single-sided position: {error}", exc_info=True)
            return {"success": False, "error": str(error)}