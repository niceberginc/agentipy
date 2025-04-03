# Crypto Market Dashboard

This example demonstrates how to use the `agentipy` framework to build a crypto market dashboard that:

- Retrieves market prices from Pyth feeds.
- Gets AI-based price predictions via Allora.
- Formats and sends styled embed messages to Discord using a webhook.

## Features

- **Price Updates:** Fetches live prices and confidence intervals for assets such as SOL/USD, BTC/USD, ETH/USD, and TRUMP/USD.
- **AI Forecast:** Retrieves short-term (5min) and longer-term (8hr) predictions for BTC and ETH.
- **Discord Integration:** Sends the updates as a rich embed message to a Discord channel.
- **Robust Logging & Error Handling:** Provides system notices and handles partial outages gracefully.

## Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/niceberginc/agentipy.git
   cd agentipy/examples/CryptoMarketDashboard
   ```

2. **Install Dependencies:**

   Ensure you have Python 3.8+ installed. Install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**

   Create a `.env` file (or set the environment variables in your system) with the following keys:

   - `ALLORA_API_KEY`: Your Allora API key.
   - `ALLORA_ENV`: Set to `"MAINNET"` or `"TESTNET"`.
   - `DISCORD_WEBHOOK_URL`: Your Discord webhook URL.
   - `SLEEP_INTERVAL`: (Optional) Time in seconds between updates (default is 300 seconds).
   - `EMBED_THUMBNAIL`: (Optional) URL for the embed thumbnail.
   - `FOOTER_ICON`: (Optional) URL for the embed footer icon.
   - `BOT_AVATAR`: (Optional) URL for the bot avatar image.

## Running the Script

Run the monitor script with:

```bash
python main.py
```

The script will continuously fetch market data and send updates to your configured Discord channel.

## Sample Output

The following is an example of how the Discord message might appear:

```
🌐 Crypto Market Dashboard
🔸 SOL/USD
+ Price: $114.3103
± Confidence: $0.0668
🕒 Updated: 16:32:37 UTC
🔸 BTC/USD
+ Price: $82102.5530
± Confidence: $33.9927
🕒 Updated: 16:32:38 UTC
​
​
🔸 ETH/USD
+ Price: $1784.4891
± Confidence: $0.8132
🕒 Updated: 16:32:39 UTC
🔸 TRUMP/USD
+ Price: $9.0251
± Confidence: $0.0144
🕒 Updated: 16:32:40 UTC
🔮 AI Forecast
BTC Predictions
▫️ 5min: $82047.61 (±$82047.61)
▫️ 8hr: $82747.61 (±$82747.61)
🔮 AI Forecast
ETH Predictions
▫️ 5min: $1784.39 (±$1784.39)
▫️ 8hr: $1816.56 (±$1816.56)
Market Intelligence v2.4•Today at 5:32 PM
```

## License

This project is licensed under the terms of the MIT license. See [LICENSE](../../LICENSE) for details.

## Contributing

Feel free to open issues or submit pull requests if you have improvements or bug fixes.

---