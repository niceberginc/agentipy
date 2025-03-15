# CoinGecko Chatbot

A terminal-based chatbot that interacts with the CoinGecko API to fetch cryptocurrency data. Users can query top gainers, trending tokens, token prices, and more. Results can be exported to JSON files for further analysis.

---

## Features

- **Fetch Data**:
  - Top gainers in the last hour.
  - Latest pools on the Solana network.
  - Token prices for specified Solana token addresses.
  - Trending tokens.

- **Export Data**:
  - Export fetched data to JSON files for offline analysis.

- **User-Friendly**:
  - Simple terminal interface with clear prompts.

---

## Prerequisites

1. **Python 3.8+**:
   - Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/).

2. **CoinGecko API Key**:
   - Sign up for a CoinGecko API key at [CoinGecko API](https://www.coingecko.com/en/api).
   - A **Pro API key** is required for some endpoints (e.g., top gainers, latest pools).

3. **Required Libraries**:
   - Install the required Python libraries using `pip`:
     ```bash
     pip install agentipy
     ```

---

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/coingecko-chatbot.git
   cd coingecko-chatbot
   ```

2. **Run the Chatbot**:
   ```bash
   python coingecko_chatbot.py
   ```

3. **Enter Your API Key**:
   - When prompted, enter your CoinGecko API key.

---

## Usage

### Commands
- **What are the top gainers?**:
  - Fetches the top gainers in the last hour.

- **Show me the latest pools**:
  - Fetches the latest pools on the Solana network.

- **Get token prices**:
  - Fetches token prices for specified Solana token addresses (comma-separated).

- **What are the trending tokens?**:
  - Fetches trending tokens.

- **Export Data**:
  - After fetching data, you can export it to a JSON file.

- **Exit**:
  - Type `exit` to quit the chatbot.

---

### Example Interaction

```
Enter your CoinGecko API key: YOUR_API_KEY
Welcome to the CoinGecko Chatbot! Type 'exit' to quit.

What would you like to know? What are the top gainers?
🔼 Top Gainers (1h):
{
    "top_gainers": [...],
    "message": "Success"
}
Export this data? (yes/no): yes
Data exported to top_gainers.json

What would you like to know? Get token prices.
Enter token addresses (comma-separated): So11111111111111111111111111111111111111112,EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
💲 Token Prices:
{
    "price_data": [...],
    "message": "Success"
}
Export this data? (yes/no): no

What would you like to know? exit
Goodbye!
```

---

## Troubleshooting

### Common Issues
1. **400 Bad Request**:
   - Ensure your API key is valid and has access to the required endpoints.
   - Verify that the token addresses are correct.

2. **Rate Limiting**:
   - Add a delay between requests if you encounter rate-limiting errors.

3. **Invalid Token Addresses**:
   - Use valid Solana token addresses (e.g., `So11111111111111111111111111111111111111112` for Wrapped SOL).

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## Acknowledgments
- [Agentipy](https://github.com/niceberginc/agentipy/)
- [CoinGecko API](https://www.coingecko.com/en/api) for providing cryptocurrency data.
- [LangChain](https://www.langchain.com/) for the tool framework.

---

Enjoy using the CoinGecko Chatbot! 🚀

