import logging
from typing import Any, Dict, Optional

import requests

from agentipy.agent.evm import EvmAgentKit, WalletType
from agentipy.utils.agentipy_proxy.utils import encrypt_private_key

logger = logging.getLogger(__name__)


class UniswapManager:
    """
    Manager class to handle Uniswap functionalities such as getting quotes for token swaps.
    """

    @staticmethod
    def get_quote(
        agent: EvmAgentKit,
        input_token_address: str,
        output_token_address: str,
        amount_in_raw: str,
        input_token_decimals: int = 18,
        output_token_decimals: int = 18,
        slippage: float = 0.5,
        fee_amount: Optional[
            int
        ] = 3000,  # Medium fee as default (corresponds to FeeAmount.MEDIUM in TS)
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves a quote from Uniswap for swapping between two tokens.

        :param agent: An instance of EvmAgentKit.
        :param input_token_address: The address of the input token.
        :param output_token_address: The address of the output token.
        :param amount_in_raw: The raw amount of input token to swap.
        :param input_token_decimals: The number of decimals for the input token (default: 18).
        :param output_token_decimals: The number of decimals for the output token (default: 18).
        :param slippage: The slippage tolerance percentage (default: 0.5).
        :param fee_amount: The fee amount for the pool (default: 3000 for MEDIUM).
        :return: Quote data or error details.
        """
        try:
            payload = {
                "rpc_url": agent.rpc_url,
                "inputToken": {
                    "address": input_token_address,
                    "decimals": input_token_decimals,
                },
                "outputToken": {
                    "address": output_token_address,
                    "decimals": output_token_decimals,
                },
                "amountInRaw": amount_in_raw,
                "slippage": slippage,
                "feeAmount": fee_amount,
            }

            response = requests.post(
                f"{agent.base_proxy_url}/{agent.api_version}/uniswap/base/getQuote",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "value": data.get("value"),
                    "message": data.get("message"),
                    "min_output_amount": data.get(
                        "message"
                    ),  # The TS endpoint returns the min output amount in the message field
                }
            else:
                return {"success": False, "error": data.get("error", "Unknown error")}

        except requests.exceptions.RequestException as http_error:
            logger.error(
                f"HTTP error during Uniswap quote retrieval: {http_error}",
                exc_info=True,
            )
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(
                f"Unexpected error during Uniswap quote retrieval: {error}",
                exc_info=True,
            )
            return {"success": False, "error": str(error)}

    @staticmethod
    def trade(
        agent: EvmAgentKit,
        input_token_address: str,
        output_token_address: str,
        amount_in_raw: str,
        input_token_decimals: int = 18,
        output_token_decimals: int = 18,
        slippage: float = 0.5,
        fee_amount: Optional[
            int
        ] = 3000,  # Medium fee as default (corresponds to FeeAmount.MEDIUM in TS)
    ) -> Optional[Dict[str, Any]]:
        """
        Executes a token swap on Uniswap.

        :param agent: An instance of EvmAgentKit.
        :param input_token_address: The address of the input token.
        :param output_token_address: The address of the output token.
        :param amount_in_raw: The raw amount of input token to swap.
        :param input_token_decimals: The number of decimals for the input token (default: 18).
        :param output_token_decimals: The number of decimals for the output token (default: 18).
        :param slippage: The slippage tolerance percentage (default: 0.5).
        :param fee_amount: The fee amount for the pool (default: 3000 for MEDIUM).
        :return: Transaction details or error information.
        """
        try:
            base_payload = {
                "rpc_url": agent.rpc_url,
                "inputToken": {
                    "address": input_token_address,
                    "decimals": input_token_decimals,
                },
                "outputToken": {
                    "address": output_token_address,
                    "decimals": output_token_decimals,
                },
                "amountInRaw": amount_in_raw,
                "slippage": slippage,
                "feeAmount": fee_amount,
                "chainId": agent.chain_id,
                "walletType": agent.wallet_type,
            }
            if agent.wallet_type == WalletType.PRIVY:
                print("privy")
                payload = {**base_payload, "wallet_id": agent.wallet_id}
            elif agent.wallet_type == WalletType.PRIVATE_KEY:
                print("private key")
                encrypted_private_key = encrypt_private_key(agent.private_key)
                payload = {
                    **base_payload,
                    "requestId": encrypted_private_key["requestId"],
                    "encrypted_private_key": encrypted_private_key[
                        "encryptedPrivateKey"
                    ],
                }
            elif agent.wallet_type == WalletType.CROSSMINT:
                print("crossmint")

            print("payload is: ", payload)

            response = requests.post(
                f"{"agent.base_proxy_url"}/{agent.api_version}/uniswap/base/trade",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            print("data is: ", data)
            if data.get("success"):
                return {
                    "success": True,
                    "value": data.get("value"),
                    "message": data.get("message"),
                    "transaction_hash": (
                        data.get("message").split("Hash: ")[1]
                        if "Hash: " in data.get("message", "")
                        else None
                    ),
                }
            else:
                return {
                    "success": False,
                    "error": data.get("error", "Unknown error"),
                    "details": data.get("details"),
                }

        except requests.exceptions.RequestException as http_error:
            logger.error(
                f"HTTP error during Uniswap trade execution: {http_error}",
                exc_info=True,
            )
            return {"success": False, "error": str(http_error)}
        except Exception as error:
            logger.error(
                f"Unexpected error during Uniswap trade execution: {error}",
                exc_info=True,
            )
            return {"success": False, "error": str(error)}
