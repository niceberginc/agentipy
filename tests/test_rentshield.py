import importlib.util
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Tuple
from unittest.mock import AsyncMock, patch

_rs: Any
try:
    from agentipy.tools import use_rentshield as _rs
except ImportError:
    _root = Path(__file__).resolve().parents[1]
    _mod_path = _root / "agentipy" / "tools" / "use_rentshield.py"
    _spec = importlib.util.spec_from_file_location("use_rentshield", _mod_path)
    assert _spec is not None and _spec.loader is not None
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules["use_rentshield"] = _mod
    _spec.loader.exec_module(_mod)
    _rs = _mod

RentShieldManager = _rs.RentShieldManager
is_valid_solana_pubkey = _rs.is_valid_solana_pubkey

USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
SAMPLE_WALLET = "7EcDhSYGxXyscszYEp35KHN8vvw3svAuLKTzXwCFLtV"
FAKE_SECRET_KEY = (
    "5MaiiCavjCmn9Hs1o3eznqDEhRwxo7pXiAYez7keQUviUkau"
    "RiTMD8DrESdrNjN8zd9mTmVhRvBJeg5vhyvgrAhG"
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
        self.assertFalse(is_valid_solana_pubkey("seed phrase not allowed"))

    async def test_private_key_rejected_offline(self) -> None:
        dummy_agent = SimpleNamespace(
            wallet_address=SAMPLE_WALLET, rentshield_api_key=""
        )
        with patch.object(RentShieldManager, "_request") as mock_req:
            with self.assertRaises(ValueError):
                await RentShieldManager.check_token_rug_shield(
                    dummy_agent, FAKE_SECRET_KEY
                )
            with self.assertRaises(ValueError):
                await RentShieldManager.scan_wallet_unclaimed_rent(
                    dummy_agent, FAKE_SECRET_KEY
                )
            mock_req.assert_not_called()

    async def test_check_token_and_scan_wallet_with_fallback(self) -> None:
        RentShieldManager.reset_cache()
        dummy_agent = SimpleNamespace(
            wallet_address=SAMPLE_WALLET, rentshield_api_key=""
        )
        recorded: List[Tuple[str, str, Any]] = []
        edge_url = "https://edge.rentandrugshield.example"
        steps = [
            _MockResponse(404, {}),
            _MockResponse(200, {"ok": True, "api_base": edge_url}),
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
        mod_obj = sys.modules[RentShieldManager.__module__]
        with patch.object(
            mod_obj.aiohttp,
            "ClientSession",
            side_effect=lambda **_: _MockSession(steps, recorded),
        ):
            audit = await RentShieldManager.check_token_rug_shield(
                dummy_agent, USDC_MINT
            )
            rent = await RentShieldManager.scan_wallet_unclaimed_rent(
                dummy_agent,
            )

        self.assertEqual(audit["score"], 98)
        self.assertTrue(audit["safe_to_buy"])
        self.assertTrue(rent["is_first_free_claim"])
        self.assertEqual(rent["effective_fee_bps"], 0)
        expected_body = {"wallet": SAMPLE_WALLET, "user_initiated": False}
        self.assertEqual(recorded[-1][2], expected_body)

    async def test_langchain_tools_wrappers(self) -> None:
        try:
            from agentipy.agent import SolanaAgentKit
            from agentipy.langchain.rentshield import get_rentshield_tools
        except ImportError:
            self.skipTest("langchain/agentipy runtime deps not installed")
        kit = SolanaAgentKit.__new__(SolanaAgentKit)
        kit.wallet_address = SAMPLE_WALLET
        kit.rentshield_api_key = ""
        kit.check_token_rug_shield = AsyncMock(  # type: ignore[method-assign]
            return_value={"mint": USDC_MINT, "safe_to_buy": True, "score": 99}
        )
        kit.scan_wallet_unclaimed_rent = (  # type: ignore[method-assign]
            AsyncMock(return_value={"wallet": SAMPLE_WALLET, "empty_count": 1})
        )
        tools = get_rentshield_tools(kit)
        self.assertEqual(len(tools), 2)
        payload = json.dumps({"mint": USDC_MINT})
        out1 = json.loads(await tools[0]._arun(payload))
        self.assertEqual(out1["status"], "success")
        self.assertEqual(out1["report"]["score"], 99)
        out2 = json.loads(await tools[1]._arun(""))
        self.assertEqual(out2["status"], "success")
        self.assertEqual(out2["result"]["empty_count"], 1)


if __name__ == "__main__":
    unittest.main()
