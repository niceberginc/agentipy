# Agentipy CoinGecko Explorer

Agentipy CoinGecko Explorer is a simple, asynchronous tool that leverages Agentipy’s LangChain-based CoinGecko tools to fetch, process, and explore live cryptocurrency data. This tool demonstrates how to orchestrate multiple data-fetching tasks—including trending tokens, price data, detailed token info, and top gainers—using LangGraph, and how to integrate LLM analysis with OpenAI's GPT-3.5-turbo.

## Features

- **Fetch Trending Tokens:** Retrieves trending tokens data from CoinGecko.
- **Fetch Price Data:** Extracts current price data for the top 5 tokens.
- **Token Information:** Fetches detailed token info, with fallback logic if the token address is invalid.
- **Top Gainers:** Retrieves the list of tokens with the highest gains in the last 24 hours.
- **LLM Analysis:** Integrates OpenAI’s GPT-3.5-turbo to analyze token info and generate insights.
- **State Memory Logging:** Maintains a log of workflow steps for robust debugging and traceability.

## Requirements

- Python 3.8+
- [agentipy](https://github.com/niceberginc/agentipy/)
- [langgraph](https://github.com/langchain-ai/langgraph)
- [openai](https://github.com/openai/openai-python)

## Installation

1. **Clone the repository** or add the `coingecko_explorer.py` file to your project.

2. **Install the required packages:**

   ```bash
   pip install agentipy langgraph openai
   ```

3. **Set your OpenAI API key:**

   Either set the API key in the script or export it as an environment variable:

   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   ```

## Usage

Run the tool with:

```bash
python coingecko_explorer.py
```

The program will:
- Fetch trending tokens from CoinGecko.
- Retrieve price data for the top 5 tokens.
- Fetch detailed token info for the first token, using fallback data if necessary.
- Fetch top gainers data.
- Attempt an LLM analysis using OpenAI's GPT-3.5-turbo.
- Print summaries including trending tokens, price data, a minimal token info summary, LLM analysis, and a memory history log.

## Example Output

```
Trending Tokens:
- ID: pi-network, Name: Pi Network, Symbol: PI
- ID: ondo-finance, Name: Ondo, Symbol: ONDO
- ID: bitcoin, Name: Bitcoin, Symbol: BTC
- ID: solana, Name: Solana, Symbol: SOL
- ID: ancient8, Name: Ancient8, Symbol: A8

Price Data for 5 Tokens:
null

Minimal Final Token Info:
{
  "id": "pi-network",
  "name": "Pi Network",
  "symbol": "PI",
  "price": 1.3927342821443367,
  "market_cap": "$9,818,605,388"
}

LLM Analysis:
None

Memory History:
- Fetched trending tokens
- Fetched price data for 5 tokens
- Token address 'pi-network' is not a valid Solana address. Using token item data instead.
- Fetched top 24h gainers
```

## Contributing

Contributions, issues, and feature requests are welcome! For more details, please visit [Agentipy's GitHub repository](https://github.com/niceberginc/agentipy/).

