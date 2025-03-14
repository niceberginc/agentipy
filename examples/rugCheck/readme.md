

# RugCheck CLI Tool

The **RugCheck CLI Tool** is a command-line interface (CLI) application that allows users to fetch and display RugCheck reports for tokens by entering their **Contract Address (CA)**. The tool uses the RugCheck API to provide detailed information about a token's risks, score, and LP lockers.

---

## Features

- **Fetch RugCheck Reports**:
  - Get a detailed report for a token, including its risk score, risks, and creator tokens.
- **Fetch LP Lockers**:
  - Retrieve information about the token's LP lockers and total locked value.
- **User-Friendly Output**:
  - Display results in an easy-to-read format.
- **Error Handling**:
  - Provide clear error messages for invalid inputs or API issues.

---

## Prerequisites

- Python 3.7 or higher.
- An API key from [RugCheck](https://rugcheck.xyz/).

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/rugcheck-cli.git
   cd rugcheck-cli
   ```

2. **Install Dependencies**:
   ```bash
   pip install aiohttp
   ```

3. **Set Up Your API Key**:
   - Replace `YOUR_API_KEY` in the `rugcheck_cli.py` script with your actual RugCheck API key.

---

## Usage

Run the script from the command line:

```bash
python rugcheck_cli.py
```

### Example Inputs

- **Wrapped SOL (Solana)**:
  ```
  So11111111111111111111111111111111111111112
  ```

- **USDC (Solana)**:
  ```
  EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
  ```

- **Raydium (Solana)**:
  ```
  4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R
  ```

### Example Output

#### Valid Input:
```
Enter the Contract Address (CA) of the token.
Example CA: So11111111111111111111111111111111111111112 (Wrapped SOL)
Your input: So11111111111111111111111111111111111111112

Fetching RugCheck report...

Token Report for So11111111111111111111111111111111111111112:
  - Program: None
  - Type: None
  - Risks: 0 risks found
  - Score: 0/100
  - Creator Tokens: None

LP Lockers:
No LP lockers found for this token.
```

#### Invalid Input:
```
Enter the Contract Address (CA) of the token.
Example CA: So11111111111111111111111111111111111111112 (Wrapped SOL)
Your input: SOL

Fetching RugCheck report...

Error: 400, message='Bad Request', url='https://api.rugcheck.xyz/v1/tokens/SOL/report/summary'
Please ensure you entered a valid Contract Address (CA).
Example CA: So11111111111111111111111111111111111111112 (Wrapped SOL)
```

---

## Troubleshooting

### Common Issues

1. **Invalid Contract Address**:
   - Ensure the contract address is valid and supported by the RugCheck API.
   - Example: `So11111111111111111111111111111111111111112` (Wrapped SOL).

2. **API Key Issues**:
   - Ensure your API key is valid and has the necessary permissions.

3. **Network Issues**:
   - Check your internet connection and ensure the RugCheck API is accessible.

---

## Contributing

Contributions are welcome! If you'd like to improve this tool, please:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [RugCheck](https://rugcheck.xyz/) for providing the API.
- [aiohttp](https://docs.aiohttp.org/) for enabling asynchronous HTTP requests.

---

Let me know if you need further assistance or additional features!