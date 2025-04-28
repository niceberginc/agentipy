## Agentipy Pyth Oracle Tool

A production-ready Pyth Network integration tool for the Agentipy framework, providing real-time, on-chain-verified price feeds for decentralized applications.

---

## Features

- 🏗️ **Agentipy-Compatible**: Seamlessly integrates as a tool within the Agentipy framework.
- ⚡ **Async-First**: Fully asynchronous implementation for non-blocking performance.
- 🔍 **All Feeds Supported**: Works with every Pyth Network price feed.
- 🛡️ **Robust Error Handling**: Graceful fallbacks for network issues and invalid addresses.
- 📊 **Confidence Reporting**: Returns price with ±confidence interval for data quality checks.
- 🔄 **Auto Connection Management**: Opens and closes RPC connections automatically.

---

## Installation

Ensure you have Python 3.8+ and pip installed, then:

```bash
pip install agentipy
```

> **Optional**: To run the advanced example (`main2.py`) with LangChain integration, also install:
>
> ```bash
> pip install langchain-openai langchain-core langchain-community python-dotenv
> ```

---

## Usage Overview

Code samples are provided in the repository as:

- **main1.py**: Fetch multiple Pyth feeds concurrently and print price with confidence interval.
- **main2.py**: Combine Pyth feeds with a LangChain/OpenAI agent for automated market analysis.

Refer to each script for detailed implementation and sample outputs.

---

## Feed Configuration

| Feed      | Pythnet Address                             |
|-----------|---------------------------------------------|
| SOL/USD   | H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG |
| BTC/USD   | GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU |
| ETH/USD   | JBu1AL4obBcCMqKBBxhpWCNUt136ijcuMZLFvTP7iWdB |
| AAVE/USD  | 3wDLxH34Yz8tGjwHszQ2MfzHwRoaQgKA32uq2bRpjJBW |
| AEVO/USD  | 26emwftTvy4CcXUcPYCHF9PcPHar4kYKfzwM1onYHBCN |

Custom feeds can be provided by any valid Pyth mint address.

---

## Advanced Configuration (main2.py)

The `main2.py` script demonstrates:
1. **Environment Setup** via `.env` (OPENAI_API_KEY)
2. **Address Validation** using on-chain checks (PythPriceAccount)
3. **LangChain Agent** with DuckDuckGoSearch for real-time market news
4. **Automated Analysis** combining on-chain price, confidence interval, and external insights

See the `main2.py` docstring and comments for step-by-step instructions.

---

## Error Handling

Handle common exceptions when calling `PythManager.get_price`:

```python
try:
    data = await PythManager.get_price(mint_address)
except ValueError:
    # Invalid address
except ConnectionError:
    # RPC endpoint unreachable
# Always verify: data['status'] == 'TRADING'
```

---

## Best Practices

1. **Cache results** to reduce RPC calls.
2. **Check status** (`TRADING`) before using price.
3. **Monitor confidence intervals** for data anomalies.
4. **Graceful reconnection** on network failures.

---

## Troubleshooting

| Error                     | Solution                                                    |
|---------------------------|-------------------------------------------------------------|
| Invalid mint address      | Verify on [Pyth Explorer](https://pyth.network/price-feeds/) |
| `NOT_TRADING` status      | Ensure feed is active on Pythnet                            |
| Connection timeout        | Check `PYTHNET_HTTP_ENDPOINT` and network connectivity      |

---

For full API reference, see [Agentipy Tools Source](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_pyth.py).

