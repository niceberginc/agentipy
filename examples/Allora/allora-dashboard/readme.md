# Allora Prediction Web Interface Example

![alt text](image.png)
A Flask web application demonstrating integration with Allora Network's prediction capabilities using Agentipy SDK.

## Features

- Real-time price predictions for BTC/ETH
- Dual timeframe predictions (5-min and 8-hour)
- Dark/light mode toggle
- Interactive UI with loading states
- Error handling and activity logging
- Topic discovery from Allora Network

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/niceberginc/agentipy.git
cd agentipy/examples
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```ini
ALLORA_API_KEY=UP-your-key-here
# ALLORA_ENV=TESTNET  # Uncomment for testnet
```

4. Run the application:
```bash
python app.py
```

Access the interface at: `http://localhost:5000`

## API Configuration

| Environment Variable | Description                          | Required |
|----------------------|--------------------------------------|----------|
| `ALLORA_API_KEY`     | API key from Allora (starts with UP-) | Yes      |
| `ALLORA_ENV`         | `MAINNET` or `TESTNET`               | No       |

## Project Structure

```
examples/
├── app.py               # Main application entry point
├── requirements.txt     # Dependencies
├── README.md            # This document
└── templates/
    └── index.html       # Frontend markup
```

## Key Implementation Details

1. **Async Integration**:
```python
loop = asyncio.new_event_loop()
Thread(target=run_async_loop, daemon=True).start()
```

2. **Prediction Handler**:
```python
@app.route('/predict/<asset>/<timeframe>')
async def get_prediction(asset, timeframe):
    # Converts user input to Allora enums
    token = PriceInferenceToken[asset.upper()]
    timeframe_enum = PriceInferenceTimeframe[timeframe.upper()]
    return await allora.get_price_prediction(token, timeframe_enum)
```

3. **UI Features**:
- Dynamic dark mode using Tailwind
- Animated loading states
- Toast notifications
- Activity history tracking

## Troubleshooting Common Issues

| Symptom               | Solution                              |
|-----------------------|---------------------------------------|
| Invalid API Key       | Ensure key starts with `UP-`          |
| Network Errors        | Check ALLORA_ENV setting              |
| Missing Dependencies  | Reinstall from requirements.txt       |
| Prediction Failures   | Verify Allora network status          |

## Need Help?

- [Allora Documentation](https://docs.allora.network)
- [Agentipy GitHub Issues](https://github.com/niceberginc/agentipy/issues)
- [Example Code Walkthrough](https://github.com/niceberginc/agentipy/tree/main/examples)

---

> **Note**: This example demonstrates SDK integration and should not be used for financial decisions. Always exercise caution when working with cryptocurrency predictions.