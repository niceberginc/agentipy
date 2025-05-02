# Agentipy MCP Server & Discord Bot

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

An implementation of the Model Context Protocol (MCP) server that provides onchain tools for AI agents, including integrations for **Claude Desktop** and a **Discord Bot**. This project allows AI agents and users to interact with the Solana blockchain through a standardized interface using Agentipy.

## Overview

This project provides multiple interfaces to the powerful Agentipy Solana tools:

1.  **MCP Server for Claude Desktop:** Integrates directly with Claude Desktop, allowing Claude AI to access and execute blockchain operations.
2.  **Discord Bot:** Brings the same onchain tools to a Discord server, enabling users to execute blockchain commands directly via chat.

Both interfaces leverage the same core set of Agentipy tools to:

- Interact with Solana blockchain
- Execute transactions
- Query account information
- Manage Solana wallets
- Get price predictions
- Trade and stake tokens
- Deploy new tokens
- Get token information from CoinGecko
- Execute cross-chain bridge transactions using deBridge
- Get real-time price data from Pyth Network
- Access comprehensive token information from CoinGecko
- Monitor trending tokens and pools
- Track top gainers and market movements
- Get detailed token price data and analytics

The project implements the Model Context Protocol specification to standardize blockchain interactions for AI agents, showcasing its flexibility across different platforms.

## Prerequisites

- Python 3.8 or higher
- Solana wallet with private key
- Solana RPC URL (mainnet, testnet, or devnet)
- OpenAI API Key (optional, for certain tools)
- Allora API Key (optional, for certain tools)
- CoinGecko Pro API Key (optional, for certain tools)
- **For Claude Desktop Integration:** Claude Desktop installed
- **For Discord Bot Integration:** A Discord Account and a Discord Bot Token

## Installation

### Option 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/niceberginc/agentipy-mcp
cd agentipy-mcp

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Manual Setup

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

Install required packages:
```bash
pip install agentipy>=2.0.8 cryptography>=3.4.7 python-dotenv>=0.17.1 web3>=7.8.0 allora_sdk>=0.2.0 mcp>=1.4.0 discord.py>=2.3.2 aiohttp>=3.8.4 # Added discord.py and aiohttp
```

(Note: discord.py and aiohttp are specifically needed for the Discord Bot)

## Configuration
### Environment Setup

Create or update your `.env` file with your credentials. This file is used by both `server.py` (for Claude) and `discord_server.py` (for Discord).

```env
# Solana Configuration
SOLANA_PRIVATE_KEY=your_solana_private_key_here
RPC_URL=your_solana_rpc_url_here

# Optional API Keys
OPENAI_API_KEY=your_openai_api_key_here
ALLORA_API_KEY=your_allora_api_key_here
COINGECKO_PRO_API_KEY=your_coingecko_api_key_here

# Discord Bot Configuration (Only needed for Discord Bot)
DISCORD_TOKEN=your_discord_bot_token_here
```

Note: Replace the placeholder values (`your_..._here`) with your actual keys and URLs.

### Getting a Discord Bot Token

To run the Discord bot, you need to create a bot application and get its token. Keep this token private!

1.  Go to the Discord Developer Portal.
2.  Log in with your Discord account.
3.  Click "New Application" in the top right corner.
4.  Give your application a name (e.g., "Agentipy Solana Bot") and click "Create".
5.  In the left sidebar, click on "Bot".
6.  Click "Add Bot". Confirm by clicking "Yes, Do it!".
7.  Under the "TOKEN" section, click "Reset Token" if it's the first time or if you need a new one.
8.  Click "Copy" to copy your bot's token. This is the value you will put in the `DISCORD_TOKEN` field in your `.env` file.
9.  **IMPORTANT:** Scroll down to the "Privileged Gateway Intents" section. Enable the **"Message Content Intent"**. This is required for the bot to read commands like `!mcp`. Save Changes.

### Adding the Discord Bot to Your Server

Once you have your bot token:

1.  In the Discord Developer Portal, go back to the "OAuth2" section in the left sidebar, then click on "URL Generator".
2.  Under "SCOPES", select `bot` and `applications.commands`.
3.  Under "BOT PERMISSIONS", select the minimum required permissions. `Send Messages` and `Read Message History` are generally sufficient for basic command response. You might need more depending on future features. `Use Slash Commands` is also necessary.
4.  Copy the generated URL at the bottom.
5.  Paste this URL into your web browser.
6.  Select the Discord server you want to add the bot to from the dropdown and click "Authorize".
7.  Complete the CAPTCHA if prompted.
8.  The bot should now appear in your server's member list (likely offline until you run the script).

## Running the Applications

After following the Installation and Configuration steps:

### Running the MCP Server for Claude Desktop (`server.py`)

This requires configuring Claude Desktop to launch `server.py` using its built-in MCP integration.

1.  **Locate the Claude Desktop Configuration File**
    *   **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
    *   **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
    *   **Linux:** `~/.config/Claude/claude_desktop_config.json`

2.  **Add the Configuration**
    Create or edit the configuration file and add the following JSON. Make sure to use the correct **absolute path** to `run_mcp.sh` (or `run_mcp.bat` on Windows).

    ```json
    {
      "mcpServers": {
        "agentipy": {
          "command": "/path/to/your/agentipy-mcp/run_mcp.sh",  # Replace with absolute path to run_mcp.sh or run_mcp.bat
          "env": {
            "RPC_URL": "your_solana_rpc_url_here",
            "SOLANA_PRIVATE_KEY": "your_private_key_here",
            "OPENAI_API_KEY": "your_openai_api_key",
            "ALLORA_API_KEY": "your_allora_api_key",
            "COINGECKO_PRO_API_KEY": "your_coingecko_api_key"
         },
         "disabled": false,
         "autoApprove": ["GET_BALANCE", "GET_PRICE_PREDICTION"]
        }
      }
    }
    ```

    (Note: The `env` section in `claude_desktop_config.json` can be left empty if you rely on the `.env` file read by `run_mcp.sh`/.bat, which is the recommended approach.)

3.  **Restart Claude Desktop**
    Restart Claude Desktop for the configuration to take effect and for it to attempt launching the MCP server.

### Running the Agentipy MCP Discord Bot (`discord_server.py`)

Ensure you have completed the installation steps and configured the `.env` file with `SOLANA_PRIVATE_KEY`, `RPC_URL`, and `DISCORD_TOKEN`.

1.  Activate your virtual environment:

    ```bash
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

2.  Run the discord bot script:

    ```bash
    python discord_server.py
    ```

The bot should come online in your Discord server.

## Project Structure
```
agentipy-mcp/
├── server.py          # Main entry point for Claude Desktop MCP server
├── discord_server.py  # Main entry point for Discord Bot
├── run_mcp.sh         # Helper script to run server.py (Unix/Mac)
├── run_mcp.bat        # Helper script to run server.py (Windows)
├── requirements.txt   # Dependencies
└── .env               # Environment variables
```
## Available Tools

The project provides the following blockchain tools, accessible via both Claude Desktop (when integrated) and the Discord Bot:

### Native Solana Actions

*   **GET_BALANCE** - Check wallet balance
*   **TRANSFER** - Transfer tokens between wallets
*   **DEPLOY_TOKEN** - Deploy new tokens on Solana

### Allora Actions

*   **GET_PRICE_PREDICTION** - Get price predictions
*   **GET_ALL_TOPICS** - Get available topics

### Jupiter Actions

*   **STAKE_WITH_JUP** - Stake tokens using Jupiter
*   **TRADE_WITH_JUP** - Trade tokens using Jupiter

### DeBridge Actions

*   **CREATE_DEBRIDGE_TRANSACTION** - Create a cross-chain bridge transaction using deBridge Liquidity Network API
*   **EXECUTE_DEBRIDGE_TRANSACTION** - Execute a cross-chain bridge transaction using deBridge Liquidity Network API
*   **CHECK_TRANSACTION_STATUS** - Check the status of a cross-chain bridge transaction using deBridge Liquidity Network API

### Pyth Actions

*   **PYTH_GET_PRICE** - Get the price of a coin from Pyth

### CoinGecko Actions

*   **COINGECKO_GET_TOKEN_INFO** - Get token information from CoinGecko
*   **COINGECKO_GET_COIN_PRICE_VS** - Get the price of a coin in a specific currency from Coingecko
*   **COINGECKO_GET_TOP_GAINERS** - Get the top gainers from Coingecko
*   **COINGECTO_GET_TRENDING_POOLS** - Get the trending pools from Coingecko
*   **COINGECKO_GET_TRENDING_TOKENS** - Get the trending tokens from Coingecko
*   **COINGECKO_GET_TOKEN_PRICE_DATA** - Get token price data from Coingecko
*   **COINGECKO_GET_LATEST_POOLS** - Get the latest pools from Coingecko

## Using the Discord Bot

Once the `discord_server.py` script is running and the bot is online in your server:

*   **List Available Actions:** Use the slash command `/mcp_help`. The bot will list all available actions and a brief description.
*   **Execute Actions (Classic Command):** Use the `!mcp` prefix followed by the action name and space-separated parameters.
    *   **Syntax:** `!mcp <ACTION_NAME> [param1] [param2] ...`
    *   **Example:** `!mcp COINGECKO_GET_TOP_GAINERS 24h 5`
    *   **Example:** `!mcp GET_BALANCE`
*   **Execute Actions (Slash Commands):** Each available MCP action is also exposed as a slash command, prefixed with `/mcp_`.
    *   **Syntax:** `/mcp_<action_name> params:"param1 param2 ..."` (parameters are passed as a single string for now)
    *   **Example:** `/mcp_coingecko_get_top_gainers params:"24h 5"`
    *   **Example:** `/mcp_get_balance`

The bot will respond with the result, formatted as JSON, potentially split into multiple messages if the output is large.

## Security Considerations

*   **Private Key:** Your Solana private key grants full control over the associated wallet. Keep it extremely secure. Use environment variables (`.env`) and ensure this file is never committed to version control.
*   **Dedicated Wallet:** Strongly consider using a dedicated, separate Solana wallet specifically for the operations performed by the AI agent or Discord bot. This limits the potential financial risk if there are errors or unexpected behavior.
*   **Discord Bot Token:** Your Discord bot token allows anyone who has it to control your bot. Treat it with the same care as your private key.
*   **Discord Server Permissions:** Be mindful of who has access to the Discord server where the bot operates, especially if you use it with a wallet containing significant funds. Consider using the bot only in private servers or channels with trusted users.
*   **`autoApprove` (Claude Desktop):** Carefully review the `autoApprove` list in `claude_desktop_config.json`. Financially significant actions like `TRANSFER` or `TRADE_WITH_JUP` should **not** be in this list.
*   **Monitoring:** Regularly monitor the activity of the Solana wallet used by the bot/AI.
*   **Testnets:** Always test new configurations and complex operations on devnet or testnet before using mainnet.

## Troubleshooting

If you encounter issues:

*   Verify your Solana private key is correct and corresponds to the correct network (mainnet/testnet/devnet) for your `RPC_URL`.
*   Check that your `RPC_URL` is correct and accessible.
*   Ensure all dependencies are installed correctly (`pip install -r requirements.txt`).
*   Verify your `.env` file contains the correct credentials for the application you are trying to run (`SOLANA_PRIVATE_KEY`, `RPC_URL`, `DISCORD_TOKEN` if running the bot).
*   **For Claude Desktop:** Check Claude Desktop logs for error messages related to the MCP server startup or communication. Ensure the `command` path in `claude_desktop_config.json` is correct and executable.
*   **For Discord Bot:**
    *   Check the console output where you ran `python discord_server.py` for errors.
    *   Verify the `DISCORD_TOKEN` in your `.env` is correct.
    *   Ensure the bot is online in the Discord server.
    *   Check that the "Message Content Intent" is enabled for your bot in the Discord Developer Portal.
    *   Ensure the bot has the necessary permissions (Send Messages, Use Slash Commands) in the channel you are using it in.

## Dependencies

Key dependencies include:

*   `agentipy` - Solana blockchain interaction
*   `python-dotenv` - Environment management
*   `mcp` - Model Context Protocol framework
*   `discord.py` - Discord API wrapper (for `discord_server.py`)
*   `cryptography` - Cryptographic primitives (dependency of agentipy/web3)
*   `web3` - Ethereum interaction (dependency, potentially for utility or future use)
*   `allora_sdk` - Allora integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/amazing-feature`)
3.  Commit your changes (`git commit -m 'Add some amazing feature'`)
4.  Push to the branch (`git push origin feature/amazing-feature`)
5.  Open a Pull Request

## License

This project is licensed under the MIT License.
