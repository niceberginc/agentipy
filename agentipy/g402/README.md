# G402 Solana Micropayment Protocol with Agentipy

This project is a complete Python implementation of the HTTP 402 Payment Required protocol using a direct on-chain Solana micropayment flow.

It has been fully integrated with the `agentipy` framework, providing a reusable `G402DataFetcher` tool that allows autonomous Solana agents to interact with payment-gated APIs.

## Key Features

-   **Agentipy Integration**: The client logic is packaged as a native `agentipy` tool, making it easy for agents to purchase access to protected data.
-   **Clean SDK Architecture**: The server-side logic is contained in a `SolanaPaymentGuard`, making it simple to protect any FastAPI endpoint.
-   **Modern Solana Transactions**: Uses Versioned Transactions and priority fees to ensure fast and reliable transaction processing.
-   **Robust Confirmation**: The agent's tool waits for `Finalized` commitment, preventing timeouts and ensuring payment certainty.
-   **Replay Attack Protection**: The server validates and stores unique payment references to prevent a single payment from being used multiple times.

## How It Works

1.  The `run_agent.py` script initializes a `SolanaAgentKit` and instructs it to use the `G402DataFetcher` tool to access a protected URL.
2.  The `server.py`, protected by the `SolanaPaymentGuard`, receives the request and returns a **`402 Payment Required`** response containing payment details (receiver, amount, reference).
3.  The `G402DataFetcher` tool handles the 402 response, uses the agent's wallet to construct and send a Solana transaction, and waits for it to be finalized.
4.  Once confirmed, the tool automatically retries the request with the transaction signature and reference in the headers as proof of payment.
5.  The `SolanaPaymentGuard` verifies the transaction on-chain. If valid, it allows the request to proceed.
6.  The server returns a **`200 OK`** response with the premium data, which is then returned to the agent.

## Setup Guide

### 1. Clone & Navigate

```bash
git clone https://github.com/agentipy/agentipy/g402
cd g402
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# On macOS/Linux:
source .venv/bin/activate

# On Windows PowerShell:
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file and copy the contents of `.env.example` into it. Fill in your server's public key and your client's base58 private key.

### 5. Add the Custom Tool to Agentipy

You must place the `use_g402.py` tool inside the installed `agentipy` library.

First, find the library's location:
```bash
pip show agentipy
```


## Running the Application

You must run the server and the agent in two separate terminals. Ensure the virtual environment is activated in both.

### Terminal 1: Start the Server

```bash
uvicorn server:app --reload
```

### Terminal 2: Run the Agent

Once the server is running, execute the agent script:

```bash
python run_agent.py
```

The agent will proceed through the entire payment flow, printing its status at each step and displaying the final unlocked data.
