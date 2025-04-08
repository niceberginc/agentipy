import logging
from typing import Optional

from allora_sdk.v2.api_client import (AlloraAPIClient, AlloraInference,
                                      AlloraTopic, ChainSlug,
                                      PriceInferenceTimeframe,
                                      PriceInferenceToken, SignatureFormat)

from agentipy.agent import SolanaAgentKit

logger = logging.getLogger(__name__)

class AlloraManager:
    def __init__(self, agent: SolanaAgentKit, base_api_url: Optional[str] = "https://api.upshot.xyz/v2", chain: ChainSlug = ChainSlug.TESTNET):
        """
        Initialize the AlloraManager with the given agent and chain environment.

        :param agent: The SolanaAgentKit instance containing the API key.
        :param chain: The blockchain network to use (ChainSlug.TESTNET or ChainSlug.MAINNET).
        """
        self.client = AlloraAPIClient(
            chain_slug=chain,
            api_key=agent.allora_api_key,
            base_api_url=base_api_url
        )
        logger.info(f"AlloraManager initialized with API key: {self.client}")

    async def get_price_prediction(
        self, asset: PriceInferenceToken, timeframe: PriceInferenceTimeframe, 
        signature_format: SignatureFormat = SignatureFormat.ETHEREUM_SEPOLIA
    ):
        """
        Fetch a future price prediction for BTC or ETH for a given timeframe (5m or 8h) from the Allora Network.

        :param asset: The crypto asset symbol (e.g., PriceInferenceToken.BTC or PriceInferenceToken.ETH).
        :param timeframe: The prediction timeframe (PriceInferenceTimeframe.FIVE_MINUTES or PriceInferenceTimeframe.EIGHT_HOURS).
        :param signature_format: The blockchain signature format (default: ETHEREUM_SEPOLIA).
        :return: A dictionary containing the predicted price and confidence interval.
        """
        try:
            inference: AlloraInference = await self.client.get_price_inference(
                asset=asset, timeframe=timeframe, signature_format=signature_format
            )

            return {
                "price_prediction": inference.inference_data.network_inference_normalized,
                "confidence_interval": inference.inference_data.confidence_interval_values_normalized,
                "status": "PREDICTED",
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Allora API request failed. Error: {str(e)}",
            }

    async def get_all_topics(self):
        """
        Fetch all available inference topics from Allora.

        :return: A list of available topics.
        """
        try:
            logger.info(f"AlloraManager initialized with API key: {self.client}")
            topics: list[AlloraTopic] = await self.client.get_all_topics()
            return {"topics": topics}
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Error fetching topics: {str(e)}",
            }

    async def get_inference_by_topic_id(self, topic_id: int):
        """
        Fetch inference data for a specific topic ID.

        :param topic_id: The topic ID for which to fetch inference data.
        :return: The inference data for the given topic.
        """
        try:
            inference: AlloraInference = await self.client.get_inference_by_topic_id(topic_id)
            return {
                "inference_data": inference.inference_data.network_inference_normalized,
                "confidence_interval": inference.inference_data.confidence_interval_values_normalized,
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Error fetching inference: {str(e)}",
            }
