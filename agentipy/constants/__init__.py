import struct

from solders.pubkey import Pubkey  # type: ignore

# Common token addresses used across the toolkit
TOKENS = {
    "USDC": Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"),  
    "USDT": Pubkey.from_string("Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"),
    "USDS": Pubkey.from_string("USDSwr9ApdHk5bvJKMjzff41FfuX8bSxdKcR81vTwcA"),
    "SOL": Pubkey.from_string("So11111111111111111111111111111111111111112"),
    "jitoSOL": Pubkey.from_string("J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn"),
    "bSOL": Pubkey.from_string("bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1"),
    "mSOL": Pubkey.from_string("mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So"),
    "BONK": Pubkey.from_string("DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"),
}

DEFAULT_OPTIONS = {
    "SLIPPAGE_BPS": 300,  # Default slippage tolerance in basis points (300 = 3%)
    "TOKEN_DECIMALS": 9,  # Default number of decimals for new tokens
}

JUP_API = "https://quote-api.jup.ag/v6"

LAMPORTS_PER_SOL = 1_000_000_000

# Pumpfun constants
EXPECTED_DISCRIMINATOR = struct.pack("<Q", 6966180631402821399)
TOKEN_DECIMALS = 6

PUMP_PROGRAM = Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")
PUMP_GLOBAL = Pubkey.from_string("4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf")
PUMP_EVENT_AUTHORITY = Pubkey.from_string("Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1")
PUMP_FEE = Pubkey.from_string("CebN5WGQ4jvEPvsVU4EoHEpgzq1VV7AbicfhtW4xC9iM")
PUMP_LIQUIDITY_MIGRATOR = Pubkey.from_string("39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg")
SYSTEM_PROGRAM = Pubkey.from_string("11111111111111111111111111111111")
SYSTEM_TOKEN_PROGRAM = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
SYSTEM_ASSOCIATED_TOKEN_ACCOUNT_PROGRAM = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
SYSTEM_RENT = Pubkey.from_string("SysvarRent111111111111111111111111111111111")

BASE_PROXY_URL = "https://api.agentipy.fun"
API_VERSION = "v1"
DEBRIDGE_API_URL = "https://dln.debridge.finance/v1.0"