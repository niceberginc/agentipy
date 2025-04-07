# Agentipy Pyth Oracle Tool

A production-ready Pyth Network integration tool for the Agentipy framework, providing real-time price feeds for DeFi applications.

## Features

- 🏗️ Built as an Agentipy-compatible tool
- ⚡ Async-first implementation for high performance
- 🔍 Supports all Pyth Network price feeds
- 🛡️ Comprehensive error handling
- 📊 Confidence interval reporting
- 🔄 Automatic connection management

## Installation

Ensure you have Agentipy installed, then add the Pyth dependency:

```bash
pip install agentipy
```

## Usage

### Importing the Tool

```python
from agentipy.tools.use_pyth import PythManager
```

### Basic Example

```python
async def get_sol_price():
    result = await PythManager.get_price("H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG")
    if result["status"] == "TRADING":
        print(f"SOL Price: ${result['price']:.4f} ± {result['confidence_interval']:.4f}")
```

### Example Output

```bash
$ python pyth_example.py

Fetching SOL/USD price...
SOL/USD:
  Price: $126.4243
  Confidence: ±$0.0646

Fetching BTC/USD price...
BTC/USD:
  Price: $85257.2530
  Confidence: ±$32.6970
```

## Feed Configuration

The tool works with any Pyth Network feed address. Common addresses:

| Feed      | Pythnet Address                             |
|-----------|---------------------------------------------|
| SOL/USD   | H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG |
| BTC/USD   | GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU |
| ETH/USD   | JBu1AL4obBcCMqKBBxhpWCNUt136ijcuMZLFvTP7iWdB |

## Advanced Usage

### Concurrent Price Fetching

```python
async def fetch_multiple_prices():
    addresses = [
        "H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG",  # SOL
        "GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU"   # BTC
    ]
    tasks = [PythManager.get_price(addr) for addr in addresses]
    return await asyncio.gather(*tasks)
```

### Error Handling

```python
try:
    price_data = await PythManager.get_price(mint_address)
except ValueError as e:
    print(f"Invalid mint address: {e}")
except Exception as e:
    print(f"Network error: {e}")
```

## Integration Guide

1. **Initialize in your Agent**:
```python
from agentipy import Agent
from agentipy.tools.use_pyth import PythManager

class MyAgent(Agent):
    async def get_prices(self):
        return await PythManager.get_price(...)
```

2. **Using in workflows**:
```python
async def trading_strategy():
    sol_price = await PythManager.get_price(SOL_ADDRESS)
    if sol_price["status"] == "TRADING":
        # Execute strategy logic
```

## Best Practices

1. Cache prices when possible to reduce RPC calls
2. Always check the `status` field before using prices
3. Monitor confidence intervals for data quality
4. Handle connection errors gracefully

## Troubleshooting

| Error | Solution |
|-------|----------|
| `Invalid mint address` | Verify address on [Pyth Explorer](https://pyth.network/price-feeds/) |
| `NOT_TRADING` status | Check if feed is active on current network |
| Connection timeout | Ensure PYTHNET_HTTP_ENDPOINT is accessible |


---

For complete documentation, see [Agentipy Tools Reference](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/use_pyth.py)