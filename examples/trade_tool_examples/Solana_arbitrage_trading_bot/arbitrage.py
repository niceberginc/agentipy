import asyncio
import aiohttp
import os
import json
from solders.pubkey import Pubkey
from agentipy.agent import SolanaAgentKit
from agentipy.tools.get_token_data import TokenDataManager
from agentipy.tools.trade import TradeManager
from agentipy.tools.get_balance import BalanceFetcher
from spl.token.async_client import AsyncToken
from spl.token.constants import TOKEN_PROGRAM_ID
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- 1. Configuration and Initialization ---

SOL_MINT = Pubkey.from_string("So11111111111111111111111111111111111111112")
JUP_API = "https://quote-api.jup.ag/v6"
RAYDIUM_API = "https://api.raydium.io/v2/main/price"
DEXSCREENER_API = "https://api.dexscreener.com/latest/dex/tokens/"
COINGECKO_TRENDING_TOKENS_API = "https://api.coingecko.com/api/v3/search/trending"
SLIPPAGE_BPS = 50
PROBE_AMOUNT = 1 * 10**8  # 0.1 SOL in lamports
PROBE_AMOUNT_JUP = 1 * 10**6  # 0.000001 SOL
FEE_PER_TRADE = 0.000005  # Typical Solana tx fee
ATA_RENT = 0.00203928  # Minimum rent for token account

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY environment variable not set.")

agent = SolanaAgentKit(
    private_key=PRIVATE_KEY,
    rpc_url="https://api.mainnet-beta.solana.com"
)

# --- 2. Helper Functions ---

async def get_jupiter_quote(session, input_mint, output_mint, amount, retries=3):
    url = f"{JUP_API}/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}&slippageBps={SLIPPAGE_BPS}"
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Jupiter: Error fetching quote: HTTP {response.status}")
                    return None
                return await response.json()
        except Exception as e:
            print(f"Jupiter: Network error on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(1)
    return None

async def get_raydium_price(session, token_mint):
    try:
        async with session.get(RAYDIUM_API) as response:
            if response.status != 200:
                print(f"Raydium: Error fetching price: HTTP {response.status}")
                return None
            data = await response.json()
            price = data.get(str(token_mint))
            return float(price) if price else None
    except Exception as e:
        print(f"Raydium: Network error: {e}")
        return None

async def get_dexscreener_price(session, token_mint):
    url = f"{DEXSCREENER_API}{token_mint}"
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"DEX Screener: Error fetching price: HTTP {response.status}")
                return None
            data = await response.json()
            sol_pairs = [pair for pair in data.get("pairs", []) if pair["chainId"] == "solana" and pair["quoteToken"]["address"] == str(SOL_MINT)]
            prices = {pair["dexId"]: float(pair["priceNative"]) for pair in sol_pairs if pair["dexId"] in ["raydium", "orca"] and 0.001 < float(pair["priceNative"]) < 10}
            return prices if prices else None
    except Exception as e:
        print(f"DEX Screener: Network error: {e}")
        return None

async def get_token_decimals(mint):
    decimals = 9 if str(mint) == str(SOL_MINT) else 6  # Default to 6 for most tokens
    try:
        token = AsyncToken(agent.connection, mint, TOKEN_PROGRAM_ID, agent.wallet)
        mint_info = await token.get_mint_info()
        if mint_info:
            decimals = mint_info.decimals
    except Exception as e:
        print(f"Failed to fetch decimals for {mint}: {e}, using default {decimals}")
    return decimals

async def fetch_token_prices(token_mint, ticker="Unknown"):
    decimals = await get_token_decimals(token_mint)
    print(f"Decimals fetched for {ticker} ({token_mint}): {decimals}")
    prices = {}
    async with aiohttp.ClientSession() as session:
        amount = PROBE_AMOUNT
        jupiter_quote = await get_jupiter_quote(session, SOL_MINT, token_mint, amount)
        if jupiter_quote and "outAmount" in jupiter_quote:
            prices["Jupiter"] = (PROBE_AMOUNT / 10**9) / (int(jupiter_quote["outAmount"]) / 10**decimals)
        raydium_price = await get_raydium_price(session, token_mint)
        if raydium_price:
            prices["Raydium"] = raydium_price
        dexscreener_prices = await get_dexscreener_price(session, token_mint)
        if dexscreener_prices:
            prices.update(dexscreener_prices)
    return prices, decimals

async def check_balance(token_mint=None):
    sol_balance = await BalanceFetcher.get_balance(agent)
    token_balance = sol_balance if token_mint == SOL_MINT else await BalanceFetcher.get_balance(agent, token_mint) or 0
    print(f"Wallet Balances: SOL = {sol_balance:.7f}, Token = {token_balance:.7f}")
    return sol_balance, token_balance

async def get_trending_tokens():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(COINGECKO_TRENDING_TOKENS_API) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                trending = data.get("coins", [])
                if trending:
                    token_ids = [token["item"]["id"] for token in trending]
                    prices_url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={','.join(token_ids)}&order=market_cap_desc&per_page=100&page=1"
                    async with session.get(prices_url) as price_response:
                        if price_response.status == 200:
                            price_data = await price_response.json()
                            price_map = {item["id"]: item["current_price"] for item in price_data}
                            for token in trending:
                                token["item"]["price_usd"] = price_map.get(token["item"]["id"])
                return trending
    except Exception as e:
        print(f"CoinGecko: Error fetching trending tokens: {e}")
        return None

async def display_trending_tokens():
    trending_tokens = await get_trending_tokens()
    if not trending_tokens:
        print("Could not retrieve trending tokens.")
        return None
    print("\n--- Trending Tokens (CoinGecko) ---")
    for i, token in enumerate(trending_tokens):
        item = token["item"]
        print(f"{i+1}. {item['name']} ({item['symbol']}): Price in USD = {item['price_usd'] if item['price_usd'] else 'N/A'}")
    print("--- End Trending Tokens ---\n")
    return trending_tokens

async def fetch_token_details(token_id):
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                return None
    except Exception as e:
        print(f"Error fetching token details: {e}")
        return None

# --- 3. LangChain Agent Setup ---

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.0, google_api_key=GOOGLE_API_KEY)

trade_prompt_template = """
You are a Solana trading expert specializing in arbitrage. You are given the current prices of a specific token across different DEXes, as well as your current wallet balances in SOL and the token.

Your task is to determine if there is an arbitrage opportunity by buying the token on the DEX with the lowest price and selling it on the DEX with the highest price. Consider that each trade incurs a small transaction fee.

If the price difference between the lowest and highest DEXes could potentially provide a profit after fees, recommend performing arbitrage. Otherwise, recommend no action.

Respond with a single, clean JSON object containing:
- "action": "arbitrage" if an opportunity exists, otherwise "none".
- "buy_dex": The DEX with the lowest price.
- "sell_dex": The DEX with the highest price.
- "reason": A short explanation.

Do not include any additional text, code blocks, backticks, or formatting outside the JSON object.

Token Prices:
{token_prices}
Current Wallet Balances: SOL = {sol_balance}, Token = {token_balance}
"""

trade_prompt = PromptTemplate.from_template(trade_prompt_template)
llm_chain = LLMChain(llm=llm, prompt=trade_prompt, verbose=True)

async def generate_trading_action(token_prices, sol_balance, token_balance):
    prompt_input = {
        "token_prices": "\n".join([f"  {dex}: {price:.7f} SOL" for dex, price in token_prices.items()]),
        "sol_balance": f"{sol_balance:.7f}",
        "token_balance": f"{token_balance:.7f}"
    }
    try:
        response = llm_chain.invoke(prompt_input)
        response_text = response.get('text', '') if isinstance(response, dict) else str(response)
        cleaned_response = response_text.strip().replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Error in generate_trading_action: {e}")
        return {"action": "none", "buy_dex": "N/A", "sell_dex": "N/A", "reason": "Failed to generate trading action"}

# --- 4. Core Trading Logic ---

async def execute_trade():
    trending_tokens = await display_trending_tokens()
    if not trending_tokens:
        print("Could not fetch trending tokens. Exiting.")
        return

    while True:
        choice = input("Enter the number of the token to trade (or enter a ticker or mint address, or 'quit'): ").strip().upper()
        if choice == 'QUIT':
            return

        token_mint = None
        ticker = None

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(trending_tokens):
                token_id = trending_tokens[index]["item"]["id"]
                token_details = await fetch_token_details(token_id)
                if token_details:
                    if token_details["symbol"].upper() == "SOL" and token_details["id"] == "solana":
                        token_mint = SOL_MINT
                        ticker = "SOL"
                    elif "platforms" in token_details and "solana" in token_details["platforms"]:
                        mint_address = token_details["platforms"]["solana"]
                        try:
                            token_mint = Pubkey.from_string(mint_address)
                            ticker = token_details["symbol"].upper()
                        except Exception:
                            print("Invalid mint address.")
                    else:
                        print(f"{token_details['symbol']} not on Solana.")
                else:
                    print("Failed to fetch token details.")
            else:
                print("Invalid selection.")
        else:
            try:
                token_mint = Pubkey.from_string(choice)
                ticker = "Unknown"
            except Exception:
                ticker = choice
                token_data = TokenDataManager.get_token_data_by_ticker(ticker)
                if token_data and token_data.address:
                    token_mint = Pubkey.from_string(token_data.address)
                else:
                    print(f"No Solana token found for '{ticker}'.")

        if token_mint:
            break
        print("Please try again.")

    print(f"\nFetching prices and balance data for {ticker if ticker else token_mint}...")
    prices, decimals = await fetch_token_prices(token_mint, ticker)
    if not prices:
        print(f"No price data for {ticker if ticker else token_mint}. Skipping.")
        return

    sol_balance, token_balance = await check_balance(token_mint)
    trading_action = await generate_trading_action(prices, sol_balance, token_balance)
    print(f"Agent Decision: {trading_action}")

    max_sol = sol_balance - FEE_PER_TRADE - (ATA_RENT if token_balance == 0 else 0)
    if max_sol <= 0:
        print("Insufficient SOL for trading after fees and potential ATA creation.")
        return

    action = input("Do you want to buy or sell? (buy/sell/none): ").lower()
    if action not in ["buy", "sell"]:
        print("No trade performed.")
        return

    async with aiohttp.ClientSession() as session:
        if action == "buy":
            while True:
                try:
                    sol_to_spend = float(input(f"How much SOL to spend buying? (max: {max_sol:.7f} SOL): "))
                    if 0 < sol_to_spend <= max_sol:
                        break
                    print(f"Enter a value between 0 and {max_sol:.7f}")
                except ValueError:
                    print("Invalid input. Enter a number.")

            quote_buy = await get_jupiter_quote(session, SOL_MINT, token_mint, int(sol_to_spend * 10**9))
            if not quote_buy:
                print("No buy quote available.")
                return
            tokens_received = int(quote_buy["outAmount"]) / 10**decimals

            try:
                print(f"Buying {tokens_received:.6f} {ticker} with {sol_to_spend:.7f} SOL via Jupiter")
                signature_buy = await TradeManager.trade(
                    agent=agent,
                    output_mint=token_mint,
                    input_amount=int(sol_to_spend * 10**9),
                    input_mint=SOL_MINT,
                    slippage_bps=SLIPPAGE_BPS
                )
                print(f"Buy successful: https://explorer.solana.com/tx/{signature_buy}")
            except Exception as e:
                print(f"Buy failed: {e}")
                return

            new_sol_balance, new_token_balance = await check_balance(token_mint)
            print(f"New SOL balance: {new_sol_balance:.7f}, New {ticker} balance: {new_token_balance:.7f}")

        elif action == "sell":
            while True:
                try:
                    token_to_sell = float(input(f"How many {ticker} to sell? (max: {token_balance:.7f}): "))
                    if 0 < token_to_sell <= token_balance:
                        break
                    print(f"Enter a value between 0 and {token_balance:.7f}")
                except ValueError:
                    print("Invalid input. Enter a number.")

            quote_sell = await get_jupiter_quote(session, token_mint, SOL_MINT, int(token_to_sell * 10**decimals))
            if not quote_sell:
                print("No sell quote available.")
                return
            sol_received = int(quote_sell["outAmount"]) / 10**9

            try:
                print(f"Selling {token_to_sell:.6f} {ticker} for {sol_received:.7f} SOL via Jupiter")
                signature_sell = await TradeManager.trade(
                    agent=agent,
                    output_mint=SOL_MINT,
                    input_amount=int(token_to_sell * 10**decimals),
                    input_mint=token_mint,
                    slippage_bps=SLIPPAGE_BPS
                )
                print(f"Sell successful: https://explorer.solana.com/tx/{signature_sell}")
            except Exception as e:
                print(f"Sell failed: {e}")
                return

            new_sol_balance, new_token_balance = await check_balance(token_mint)
            print(f"New SOL balance: {new_sol_balance:.7f}, New {ticker} balance: {new_token_balance:.7f}")

# --- 5. Main Execution ---

async def main():
    print("Starting Solana Token Price Trader with Arbitrage Strategy on Mainnet...")
    while True:
        await execute_trade()
        next_action = input("\nEnter another token ticker, mint address, or 'quit' to exit: ").upper()
        if next_action == "QUIT":
            break

if __name__ == "__main__":
    asyncio.run(main())