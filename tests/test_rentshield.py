import importlib.util
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Tuple
import unittest
from unittest.mock import patch

try:
    from agentipy.tools.use_rentshield import RentShieldManager, is_valid_solana_pubkey
except ImportError:
    _MOD_PATH = Path(__file__).resolve().parents[1] / "agentipy" / "tools" / "use_rentshield.py"
    _SPEC = importlib.util.spec_from_file_location("use_rentshield", _MOD_PATH)
    assert _SPEC is not None and _SPEC.loader is not None
    import sys
    _MOD = importlib.util.module_from_spec(_SPEC)
    sys.modules['use_rentshield'] = _MOD
    _SPEC.loader.exec_module(_MOD)
    RentShieldManager = _MOD.RentShieldManager
    is_valid_solana_pubkey = _MOD.is_valid_solana_pubkey

USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
SAMPLE_WALLET = "7EcDhSYGxXyscszYEp35KHN8vvw3svAuLKTzXwCFLtV"
FAKE_SECRET_KEY = (
    "5MaiiCavjCmn9Hs1o3eznqDEhRwxo7pXiAYez7keQUviUkauRiTMD8DrESdrNjN8zd9mTmVhRvBJeg5vhyvgrAhG"
)


class _MockResponse:
    def __init__(self, status: int, payload: Dict[str, Any]) -> None:
        self.status = status
        self._payload = payload

    async def __aenter__(self) -> "_MockResponse":
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        return None

    def raise_for_status(self) -> None:
        if self.status >= 400:
            raise RuntimeError(f"HTTP {self.status}")

    async def json(self) -> Dict[str, Any]:
        return self._payload


class _MockSession:
    def __init__(
        self, steps: List[_MockResponse], recorded: List[Tuple[str, str, Any]]
    ) -> None:
        self._steps = steps
        self._recorded = recorded

    async def __aenter__(self) -> "_MockSession":
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        return None

    def request(
        self, method: str, url: str, headers: Any = None, json: Any = None
    ) -> _MockResponse:
        self._recorded.append((method, url, json))
        return self._steps.pop(0)

    def get(self, url: str, headers: Any = None) -> _MockResponse:
        self._recorded.append(("GET", url, None))
        return self._steps.pop(0)


class TestRentShieldManager(unittest.IsolatedAsyncioTestCase):
    def test_pubkey_guard_rejects_secret_keys_and_seed_phrases(self) -> None:
        self.assertTrue(is_valid_solana_pubkey(USDC_MINT))
        self.assertTrue(is_valid_solana_pubkey(SAMPLE_WALLET))
        self.assertFalse(is_valid_solana_pubkey(FAKE_SECRET_KEY))
        self.assertFalse(is_valid_solana_pubkey("seed phrase words never allowed"))

    async def test_private_key_rejected_offline(self) -> None:
        dummy_agent = SimpleNamespace(wallet_address=SAMPLE_WALLET, rentshield_api_key="")
        with patch.object(RentShieldManager, "_request") as mock_req:
            with self.assertRaises(ValueError):
                await RentShieldManager.check_token_rug_shield(dummy_agent, FAKE_SECRET_KEY)
            with self.assertRaises(ValueError):
                await RentShieldManager.scan_wallet_unclaimed_rent(dummy_agent, FAKE_SECRET_KEY)
            mock_req.assert_not_called()

    async def test_check_token_and_scan_wallet_with_fallback(self) -> None:
        RentShieldManager.reset_cache()
        dummy_agent = SimpleNamespace(wallet_address=SAMPLE_WALLET, rentshield_api_key="")
        recorded: List[Tuple[str, str, Any]] = []
        steps = [
            _MockResponse(404, {}),
            _MockResponse(200, {"ok": True, "api_base": "https://edge.rentandrugshield.example"}),
            _MockResponse(
                200,
                {
                    "ok": True,
                    "mint": USDC_MINT,
                    "symbol": "USDC",
                    "score": 98,
                    "safe_to_buy": True,
                    "verdict": "SAFE",
                    "layers_checked": 11,
                },
            ),
            _MockResponse(
                200,
                {
                    "ok": True,
                    "wallet": SAMPLE_WALLET,
                    "is_first_free_claim": True,
                    "effective_fee_bps": 0,
                    "empty_count": 2,
                    "total_reclaimable_sol": 0.004078,
                    "total_reclaimable_lamports": 4078560,
                },
            ),
        ]
        target_mod = RentShieldManager.__module__
        import sys
        mod_obj = sys.modules[target_mod]
        with patch.object(
            mod_obj.aiohttp,
            "ClientSession",
            side_effect=lambda **_: _MockSession(steps, recorded),
        ):
            audit = await RentShieldManager.check_token_rug_shield(dummy_agent, USDC_MINT)
            rent = await RentShieldManager.scan_wallet_unclaimed_rent(dummy_agent)

        self.assertEqual(audit["score"], 98)
        self.assertTrue(audit["safe_to_buy"])
        self.assertTrue(rent["is_first_free_claim"])
        self.assertEqual(rent["effective_fee_bps"], 0)
        self.assertEqual(recorded[-1][2], {"wallet": SAMPLE_WALLET, "user_initiated": False})


if __name__ == "__main__":
    unittest.main()
