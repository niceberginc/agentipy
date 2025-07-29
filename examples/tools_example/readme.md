# Agentipy Request Faucet Tools

This document provides an overview and usage examples for Solana-related tools within the `agentipy` library.

## 1. Balance Fetcher Tool

This module provides a utility class, `BalanceFetcher`, for retrieving cryptocurrency balances within the Solana ecosystem. It allows fetching the balance of native SOL or any SPL token associated with a Solana agent's wallet.

### Features

*   **Fetch SOL Balance:** Retrieve the native SOL balance of an agent's wallet.
*   **Fetch SPL Token Balance:** Retrieve the balance of any SPL token associated with an agent's wallet.
*   **Error Handling:** Provides robust error handling for balance fetching operations.

### Usage

The `BalanceFetcher` class has a static method `get_balance`.

#### Example

```python
import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.get_balance import BalanceFetcher
from solders.pubkey import Pubkey
import base58

async def main():
    # Replace with your actual private key and RPC URL
    agent = SolanaAgentKit(
        private_key="",  # Your wallet private key in base58 format
        rpc_url="https://api.devnet.solana.com" # 
    )

    try:
        # Fetch SOL balance
        sol_balance = await BalanceFetcher.get_balance(agent)
        if sol_balance is not None:
            print(f"SOL Balance: {sol_balance} SOL")
        else:
            print("Could not fetch SOL balance (account might not exist or is inaccessible).")

    except Exception as e:
        print(f"Failed to fetch SOL balance: {e}")

    # Example of fetching an SPL token balance 
     try:
         # Example: USDC token mint address on Devnet
         usdc_token_address = Pubkey.from_string("EPjFWdd5AufqSS2RmSXu3a9a9f9QyuHjeTzk7JRmXj9X")
         usdc_balance = await BalanceFetcher.get_balance(agent, token_address=usdc_token_address)
         if usdc_balance is not None:
             print(f"USDC Balance: {usdc_balance} USDC")
         else:
             print("Could not fetch USDC balance (token account might not exist).")
     except Exception as e:
         print(f"Failed to fetch USDC balance: {e}")


if __name__ == "__main__":
    asyncio.run(main())
```

#### Parameters for `get_balance`

*   `agent` (`SolanaAgentKit`): An instance of `SolanaAgentKit`.
*   `token_address` (`Optional[Pubkey]`): The SPL token mint address. If `None`, fetches SOL balance.

#### Return Value

*   `Optional[float]`: Balance in UI units, or `None` if the account doesn't exist.

#### Exceptions

*   Raises `Exception` on failure.

---

## 2. Faucet Manager Tool

This module provides a utility class, `FaucetManager`, for requesting SOL from the Solana faucet. This tool is intended for use with Solana's devnet or testnet environments.

### Features

*   **Request SOL Airdrop:** Conveniently request SOL from the faucet to fund a wallet.
*   **Transaction Confirmation:** Automatically confirms the airdrop transaction.
*   **Error Handling:** Catches and reports specific errors related to faucet requests and transaction confirmations.

### Usage

The `FaucetManager` class has a static method `request_faucet_funds`.

#### Example

```python
import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.request_faucet_funds import FaucetManager
from solders.keypair import Keypair
import base58

async def main():
    agent = SolanaAgentKit(
        private_key="",  
        rpc_url="https://api.devnet.solana.com" 
    )

    try:
        tx_signature = await FaucetManager.request_faucet_funds(agent)
        print(f"Faucet airdrop completed. Transaction Signature: {tx_signature}")
    except Exception as e:
        print(f"Faucet airdrop failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

#### Parameters for `request_faucet_funds`

*   `agent` (`SolanaAgentKit`): An instance of `SolanaAgentKit` that will receive the funds.

#### Return Value

*   `str`: The transaction signature of the successful airdrop.

#### Exceptions

*   `Exception`: If the airdrop response is malformed or other errors occur.
*   `RPCException`: If the faucet request fails due to an RPC error.

#### Important Notes

*   This tool is intended for **devnet and testnet only**.
*   Ensure your `rpc_url` points to a valid devnet or testnet endpoint.
*   The default amount requested is 5 SOL.

---

## Contribution

Contributions to these tools are welcome. Please refer to the `agentipy` project's contribution guidelines.

## License

These tools are licensed under the MIT License.
