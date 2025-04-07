import asyncio
import os
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_allora import (
    AlloraManager,
    PriceInferenceToken,
    PriceInferenceTimeframe,
    ChainSlug
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", 300))
API_ENV = os.getenv("ALLORA_ENV", "MAINNET")
CHAIN = ChainSlug.MAINNET if API_ENV.upper() == "MAINNET" else ChainSlug.TESTNET

class Predictions(BaseModel):
    btc_5min: Optional[float] = None
    eth_5min: Optional[float] = None
    btc_8hour: Optional[float] = None
    eth_8hour: Optional[float] = None
    last_updated: Optional[datetime] = None

latest_predictions = Predictions()
allora = None

app = FastAPI()

async def fetch_predictions_loop():
    global latest_predictions
    while True:
        try:
            btc_5min = await allora.get_price_prediction(PriceInferenceToken.BTC, PriceInferenceTimeframe.FIVE_MIN)
            eth_5min = await allora.get_price_prediction(PriceInferenceToken.ETH, PriceInferenceTimeframe.FIVE_MIN)
            btc_8hour = await allora.get_price_prediction(PriceInferenceToken.BTC, PriceInferenceTimeframe.EIGHT_HOURS)
            eth_8hour = await allora.get_price_prediction(PriceInferenceToken.ETH, PriceInferenceTimeframe.EIGHT_HOURS)
            
            latest_predictions.btc_5min = btc_5min
            latest_predictions.eth_5min = eth_5min
            latest_predictions.btc_8hour = btc_8hour
            latest_predictions.eth_8hour = eth_8hour
            latest_predictions.last_updated = datetime.now()
            
            logging.info(f"Updated predictions - BTC (5min): {btc_5min}, ETH (5min): {eth_5min}, "
                         f"BTC (8hour): {btc_8hour}, ETH (8hour): {eth_8hour}")
        except Exception as e:
            logging.error(f"Error fetching predictions: {str(e)}")
        await asyncio.sleep(SLEEP_INTERVAL)

@app.on_event("startup")
async def startup_event():
    global allora
    api_key = os.getenv('ALLORA_API_KEY', 'UP-Allora_Api-key')
    agent = SolanaAgentKit(allora_api_key=api_key)
    allora = AlloraManager(agent=agent, chain=CHAIN)
    asyncio.create_task(fetch_predictions_loop())

@app.get("/predictions", response_model=Predictions)
async def get_predictions():
    return latest_predictions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)