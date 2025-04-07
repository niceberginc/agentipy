# AgentiPY Allora Price Prediction Example


![AgentiPY](https://agentipy.fun/logo.png)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-green)
![Web3](https://img.shields.io/badge/Web3-6.0%2B-orange)

A production-ready FastAPI service that provides continuous price predictions for BTC and ETH using the Allora Network via the Agentipy library.

## 📖 Overview

This implementation demonstrates:
- Real-time price predictions for BTC/ETH (5min and 8hr timeframes)
- Asynchronous data fetching from Allora Network
- Continuous background updates
- REST API endpoint for prediction access
- Production-grade error handling and logging

## ✨ Features

- 🚀 Async FastAPI backend
- 🔄 Automatic prediction updates
- 🔐 Secure API key management
- 📈 Dual timeframe support (5min/8hr)
- 🌐 Mainnet/Testnet compatibility
- 📊 Structured logging
- 🛠️ Environment configuration

## ⚙️ Prerequisites

- Python 3.8+
- Agentipy (`pip install agentipy`)
- `pip` package manager
- FastAPI (`pip install fastapi`)
- Uvicorn (`pip install uvicorn`)

## 🛠️ Installation

```bash
git clone https://github.com/niceberginc/agentipy.git
cd agentipy/examples
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 🔧 Configuration

Configure via environment variables (`.env` file recommended):

```ini
# Required
ALLORA_API_KEY="your_api_key_here"

# Optional
SLEEP_INTERVAL=300  # Update frequency in seconds (default: 300)
ALLORA_ENV="MAINNET"  # MAINNET or TESTNET
```

## 🚀 Usage

Start the service:
```bash
uvicorn main:app --reload
```

Service will be available at:
- Local: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

## 🌐 API Endpoints

### GET /predictions
Retrieve latest predictions:

**Response Model (Predictions):**
```json
{
  "btc_5min": 85309.35,
  "eth_5min": 1919.23,
  "btc_8hour": 85522.42,
  "eth_8hour": 1914.92,
  "last_updated": "2025-04-01T17:01:44.750Z"
}
```

## 🛡️ Error Handling

- Automatic retry on failed API calls
- Structured error responses:
  ```json
  {
    "status": "ERROR",
    "message": "Detailed error description"
  }
  ```
- Graceful degradation during network issues

## 📝 Logging

Structured logs format:
```
2025-04-01 17:01:44,750 - INFO - Updated predictions - BTC (5min): 85309.35...
```

Log levels controlled via `logging.INFO` in code.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

## ☎️ Support

For issues/questions:
- [GitHub Issues](https://github.com/niceberginc/agentipy/issues)

---

**Note:** Replace `your_api_key_here` with actual Allora API key before deployment. Testnet recommended for development.
