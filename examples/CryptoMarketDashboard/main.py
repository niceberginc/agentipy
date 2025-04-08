import asyncio
import os
import logging
import datetime
from typing import Dict, List, Any

import aiohttp

from agentipy.tools.use_pyth import PythManager
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_allora import (
    AlloraManager,
    PriceInferenceToken,
    PriceInferenceTimeframe,
    ChainSlug
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Configuration
SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", 300))
ALLORA_ENV = os.getenv("ALLORA_ENV", "MAINNET")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CHAIN = ChainSlug.MAINNET if ALLORA_ENV.upper() == "MAINNET" else ChainSlug.TESTNET

PYTH_FEEDS: Dict[str, str] = {
    "SOL/USD": "H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG",
    "BTC/USD": "GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU",
    "ETH/USD": "JBu1AL4obBcCMqKBBxhpWCNUt136ijcuMZLFvTP7iWdB",
    "TRUMP/USD": "A8G6XyA6fSrsavG63ssAGU3Hnt2oDZARxefREzAY5axH",
}

class MarketMonitor:
    def __init__(self):
        self.agent = SolanaAgentKit(
            allora_api_key=os.getenv('ALLORA_API_KEY', 'UP-Allora_API_Key')
        )
        self.session = aiohttp.ClientSession()
        self.last_update = datetime.datetime.utcnow()

    async def close(self):
        await self.session.close()

    def _format_prediction(self, prediction_data: Dict[str, Any]) -> str:
        """Format prediction data with confidence interval"""
        try:
            price = prediction_data.get('price_prediction', 0)
            confidence = prediction_data.get('confidence_interval', [0.0])[0]
            return f"${float(price):.2f} (±${float(confidence):.2f})"
        except Exception as e:
            logging.error(f"Error formatting prediction: {str(e)}")
            return "N/A"

    async def create_embed(self, message_data: dict) -> dict:
        """Create a rich Discord embed with modern UI elements"""
        status_color = 0x00FF88 if message_data.get('status') == "success" else 0xFF3300
        timestamp = datetime.datetime.utcnow().isoformat()

        embed = {
            "title": "🌐 Crypto Market Dashboard",
            "color": status_color,
            "thumbnail": {"url": os.getenv("EMBED_THUMBNAIL", "")},
            "footer": {
                "text": "Market Intelligence v2.4",
                "icon_url": os.getenv("FOOTER_ICON", "")
            },
            "timestamp": timestamp,
            "fields": []
        }

        # Price Section
        price_fields = []
        for symbol, data in message_data.get('prices', {}).items():
            price_fields.append({
                "name": f"🔸 {symbol}",
                "value": (
                    f"```diff\n"
                    f"+ Price: ${data['price']:.4f}\n"
                    f"± Confidence: ${data['confidence']:.4f}\n"
                    f"🕒 Updated: {data['timestamp']}\n"
                    f"```"
                ),
                "inline": True
            })
        
        # Add prices in grid layout
        for i in range(0, len(price_fields), 2):
            embed["fields"].extend(price_fields[i:i+2])
            if i+2 < len(price_fields):
                embed["fields"].append({"name": "\u200b", "value": "\u200b", "inline": False})

        # Prediction Section
        if message_data.get('predictions'):
            prediction_groups = {}
            for pred in message_data['predictions']:
                key = pred['token']
                if key not in prediction_groups:
                    prediction_groups[key] = []
                prediction_groups[key].append(pred)
            
            for token, preds in prediction_groups.items():
                pred_lines = [f"**{token} Predictions**"]
                for p in preds:
                    formatted = self._format_prediction(p['data'])
                    pred_lines.append(f"▫️ {p['timeframe']}: {formatted}")
                
                embed["fields"].append({
                    "name": "🔮 AI Forecast",
                    "value": "\n".join(pred_lines),
                    "inline": False
                })

        # Warnings Section
        if message_data.get('warnings'):
            embed["fields"].append({
                "name": "⚠️ System Notices",
                "value": "\n".join([f"▫️ {warn}" for warn in message_data['warnings']]),
                "inline": False
            })

        return embed

    async def send_discord_update(self, message_data: dict):
        """Send styled embed message to Discord"""
        if not DISCORD_WEBHOOK_URL:
            logging.warning("Discord webhook not configured")
            return

        try:
            embed = await self.create_embed(message_data)
            payload = {
                "embeds": [embed],
                "username": "Crypto Sentinel",
                "avatar_url": os.getenv("BOT_AVATAR", "")
            }

            async with self.session.post(DISCORD_WEBHOOK_URL, json=payload) as resp:
                if resp.status not in (200, 204):
                    error = await resp.text()
                    logging.error(f"Discord API error: {resp.status} - {error}")
                else:
                    logging.info("Sent market update successfully")

        except Exception as e:
            logging.error(f"Notification error: {str(e)}")

    async def fetch_market_data(self) -> dict:
        """Aggregate data from all sources"""
        data = {
            "status": "success",
            "prices": {},
            "predictions": [],
            "warnings": []
        }

        # Fetch Pyth prices
        for symbol, address in PYTH_FEEDS.items():
            try:
                result = await PythManager.get_price(address)
                if result["status"] == "TRADING":
                    data["prices"][symbol] = {
                        "price": result["price"],
                        "confidence": result["confidence_interval"],
                        "timestamp": datetime.datetime.utcnow().strftime("%H:%M:%S UTC")
                    }
                else:
                    data["warnings"].append(f"{symbol} in {result['status']} status")
            except Exception as e:
                data["warnings"].append(f"{symbol} data unavailable")
                logging.error(f"Price error ({symbol}): {str(e)}")

        # Fetch Allora predictions
        try:
            allora = AlloraManager(agent=self.agent, chain=CHAIN)
            timeframes = [
                (PriceInferenceTimeframe.FIVE_MIN, "5min"),
                (PriceInferenceTimeframe.EIGHT_HOURS, "8hr")
            ]
            
            predictions = []
            for token in [PriceInferenceToken.BTC, PriceInferenceToken.ETH]:
                for timeframe, label in timeframes:
                    try:
                        prediction = await allora.get_price_prediction(token, timeframe)
                        predictions.append({
                            "token": token.name,
                            "timeframe": label,
                            "data": prediction  
                        })
                    except Exception as e:
                        data["warnings"].append(f"Prediction failed for {token.name} {label}")
                        logging.error(f"Prediction error ({token.name} {label}): {str(e)}")
            
            data["predictions"] = predictions
            
        except Exception as e:
            data["warnings"].append("Prediction service unavailable")
            logging.error(f"Allora connection error: {str(e)}")

        # Update system status
        if len(data["warnings"]) > 2:
            data["status"] = "partial_outage"
        elif len(data["warnings"]) > 0:
            data["status"] = "warning"

        return data

    async def monitor_loop(self):
        """Main monitoring loop"""
        while True:
            try:
                market_data = await self.fetch_market_data()
                await self.send_discord_update(market_data)
                logging.info(f"Sleeping for {SLEEP_INTERVAL}s...")
                await asyncio.sleep(SLEEP_INTERVAL)
                
            except Exception as e:
                logging.error(f"Critical error: {str(e)}")
                emergency_data = {
                    "status": "error",
                    "warnings": ["System malfunction - attempting recovery"]
                }
                await self.send_discord_update(emergency_data)
                await asyncio.sleep(60)

async def main():
    monitor = MarketMonitor()
    try:
        await monitor.monitor_loop()
    except KeyboardInterrupt:
        await monitor.close()
        logging.info("Graceful shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user")