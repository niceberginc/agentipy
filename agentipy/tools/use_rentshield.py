import os
import re
import time
from typing import Any, Dict, Optional
from urllib.parse import quote, urlparse

import aiohttp

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
SOLANA_PUBKEY_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
RENTSHIELD_BASE_URL = "https://rentandrugshield.com"


def is_valid_solana_pubkey(address: str) -> bool:
    """Return True if address decodes to a 32-byte base58 Solana pubkey."""
    if not isinstance(address, str):
        return False
    cleaned = address.strip()
    if not SOLANA_PUBKEY_RE.match(cleaned):
        return False
    acc = [0]
    for ch in cleaned:
        carry = BASE58_ALPHABET.find(ch)
        if carry < 0:
            return False
        for idx in range(len(acc)):
            carry += acc[idx] * 58
            acc[idx] = carry & 0xFF
            carry >>= 8
        while carry > 0:
            acc.append(carry & 0xFF)
            carry >>= 8
    leading_ones = 0
    while leading_ones < len(cleaned) and cleaned[leading_ones] == "1":
        leading_ones += 1
    return len(acc) + leading_ones == 32


def validate_public_solana_address(
    address: str,
    field_name: str = "address",
) -> str:
    """Validate public Solana address and reject private keys/mnemonics."""
    cleaned = str(address or "").strip()
    if not is_valid_solana_pubkey(cleaned):
        raise ValueError(
            f"Invalid {field_name}: expected a 32-byte base58 Solana public "
            "key. Never pass private keys or seed phrases."
        )
    return cleaned


class RentShieldManager:
    """Read-only Solana 11-layer rug check and empty ATA rent scanner."""

    BASE_URL = RENTSHIELD_BASE_URL
    _cached_live_base: Optional[str] = None
    _cached_expires_at: float = 0.0

    @classmethod
    def reset_cache(cls) -> None:
        cls._cached_live_base = None
        cls._cached_expires_at = 0.0

    @classmethod
    async def _resolve_live_base(
        cls,
        session: aiohttp.ClientSession,
    ) -> Optional[str]:
        now = time.monotonic()
        if cls._cached_live_base and cls._cached_expires_at > now:
            return cls._cached_live_base
        async with session.get(
            f"{cls.BASE_URL}/live_endpoint.json",
            headers={"Accept": "application/json"},
        ) as resp:
            if resp.status != 200:
                return None
            payload = await resp.json()
            raw_base = payload.get("api_base") or payload.get("endpoint") or ""
            candidate = str(raw_base).strip().rstrip("/")
            if not candidate:
                return None
            parsed = urlparse(candidate)
            if parsed.scheme != "https" or not parsed.netloc:
                return None
            cls._cached_live_base = candidate
            cls._cached_expires_at = now + 300.0
            return candidate

    @classmethod
    async def _request(
        cls,
        agent: Any,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        req_headers: Dict[str, str] = {"Accept": "application/json"}
        if headers:
            req_headers.update(headers)
        agent_key = getattr(agent, "rentshield_api_key", None)
        api_key = agent_key or os.getenv("RENTSHIELD_API_KEY")
        if api_key:
            req_headers["X-API-Key"] = str(api_key)

        env_base = os.getenv("RENTSHIELD_API_URL", "").strip().rstrip("/")
        cache_valid = (
            cls._cached_live_base and cls._cached_expires_at > time.monotonic()
        )
        cached_base = cls._cached_live_base if cache_valid else None
        initial_base = env_base or cached_base or cls.BASE_URL

        timeout = aiohttp.ClientTimeout(total=10.0)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.request(
                method,
                f"{initial_base}{path}",
                headers=req_headers,
                json=json_body,
            ) as resp:
                if not env_base and resp.status in (404, 405):
                    live_base = await cls._resolve_live_base(session)
                    if live_base and live_base != initial_base:
                        async with session.request(
                            method,
                            f"{live_base}{path}",
                            headers=req_headers,
                            json=json_body,
                        ) as retry_resp:
                            retry_resp.raise_for_status()
                            return dict(await retry_resp.json())
                resp.raise_for_status()
                return dict(await resp.json())

    @classmethod
    async def check_token_rug_shield(
        cls,
        agent: Any,
        mint: str,
    ) -> Dict[str, Any]:
        """Run a read-only 11-layer pre-buy rug audit on a Solana mint."""
        clean_mint = validate_public_solana_address(mint, "mint")
        data = await cls._request(
            agent,
            "GET",
            f"/api/rug-check/{quote(clean_mint, safe='')}",
        )
        score = data.get("score")
        safe_to_buy = data.get("safe_to_buy")
        if safe_to_buy is None and isinstance(score, (int, float)):
            safe_to_buy = score >= 70
        raw_checks = data.get("checks")
        checks = raw_checks if isinstance(raw_checks, list) else []
        return {
            "ok": bool(data.get("ok", True)),
            "mint": data.get("mint") or clean_mint,
            "symbol": data.get("symbol"),
            "name": data.get("name"),
            "token_program": data.get("token_program"),
            "score": score,
            "safe_to_buy": bool(safe_to_buy),
            "verdict": data.get("verdict"),
            "layers_checked": data.get("layers_checked", 11),
            "layers_passed": data.get("layers_passed"),
            "checklist_summary": data.get("checklist_summary"),
            "checks": checks,
            "report_url": f"{cls.BASE_URL}/audit/{clean_mint}",
        }

    @classmethod
    async def scan_wallet_unclaimed_rent(
        cls, agent: Any, wallet: Optional[str] = None
    ) -> Dict[str, Any]:
        """Preview reclaimable SOL rent across empty SPL & Token-2022 ATAs."""
        agent_wallet = getattr(agent, "wallet_address", None)
        fallback_wallet = str(agent_wallet) if agent_wallet else ""
        target = wallet or fallback_wallet
        clean_wallet = validate_public_solana_address(target, "wallet")
        data = await cls._request(
            agent,
            "POST",
            "/api/scan-wallet",
            headers={"Content-Type": "application/json"},
            json_body={"wallet": clean_wallet, "user_initiated": False},
        )
        fee_bps = data.get("effective_fee_bps", data.get("fee_bps", 0))
        raw_empty = data.get("empty_reclaimable")
        empty_list = raw_empty if isinstance(raw_empty, list) else []
        lamports = data.get("total_reclaimable_lamports", 0)
        return {
            "ok": bool(data.get("ok", True)),
            "wallet": data.get("wallet") or clean_wallet,
            "is_first_free_claim": bool(data.get("is_first_free_claim")),
            "effective_fee_bps": fee_bps,
            "reclaimable_count": data.get("reclaimable_count", 0),
            "empty_count": data.get("empty_count", 0),
            "dust_count": data.get("dust_count", 0),
            "active_count": data.get("active_count", 0),
            "total_reclaimable_sol": data.get("total_reclaimable_sol", 0.0),
            "total_reclaimable_lamports": lamports,
            "empty_reclaimable": empty_list,
            "claim_url": f"{cls.BASE_URL}/?wallet={clean_wallet}",
        }
