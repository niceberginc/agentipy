
from typing import Dict, List, Optional

from construct import Flag, Int64ul, Struct
from pydantic import BaseModel, field_validator
from solders.pubkey import Pubkey  # type: ignore


class BaseModelWithArbitraryTypes(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        extra = 'ignore'  # Ignore unexpected fields
        validate_assignment = True

class RiskItem(BaseModelWithArbitraryTypes):
    """
    Represents a single risk item in the RugCheck token report.
    """
    name: str
    value: Optional[str] = None
    description: str
    score: int
    level: str

class TokenCheck(BaseModelWithArbitraryTypes):
    """
    Model for token report data from RugCheck API.
    """
    tokenProgram: Optional[str] = None
    tokenType: Optional[str] = None
    risks: List[RiskItem] = []
    score: Optional[int] = None
    score_normalised: Optional[int] = None
    lpLockedPct: Optional[float] = None

    

class Locker(BaseModelWithArbitraryTypes):
    """
    Model for LP locker data.
    """
    programID: str
    tokenAccount: str
    owner: str
    uri: str
    unlockDate: int
    usdcLocked: float
    type: str

    def to_user_friendly_string(self) -> str:
        """
        Convert the locker data to a user-friendly string.
        """
        return (
            f"Locker Details:\n"
            f"  - Program ID: {self.programID}\n"
            f"  - Token Account: {self.tokenAccount}\n"
            f"  - Owner: {self.owner}\n"
            f"  - URI: {self.uri}\n"
            f"  - Unlock Date: {self.unlockDate}\n"
            f"  - USDC Locked: ${self.usdcLocked:,.2f}\n"
            f"  - Type: {self.type}"
        )

class TokenLockers(BaseModelWithArbitraryTypes):
    """
    Model for LP lockers response.
    """
    lockers: Optional[Dict[str, Locker]] = None
    total: Optional[Dict[str, float]] = None

    @field_validator('lockers', 'total', mode='before')
    @classmethod
    def handle_null_fields(cls, value):
        """Convert null fields to empty dictionaries."""
        return value or {}

    def to_user_friendly_string(self) -> str:
        """
        Convert the LP lockers data to a user-friendly string.
        """
        if not self.lockers:
            return "No LP lockers found for this token."
        
        lockers_info = "\n".join(
            f"Locker {i + 1}:\n{locker.to_user_friendly_string()}"
            for i, (_, locker) in enumerate(self.lockers.items())
        )
        total_usdc = self.total.get('totalUSDC', 0) if self.total else 0
        return (
            f"LP Lockers:\n{lockers_info}\n"
            f"Total USDC Locked: ${total_usdc:,.2f}"
        )

class TrendingToken(BaseModelWithArbitraryTypes):
    """
    Model for trending token data.
    """
    mint: str
    vote_count: int
    up_count: int

    def to_user_friendly_string(self) -> str:
        """
        Convert the trending token data to a user-friendly string.
        """
        return (
            f"Trending Token: {self.mint}\n"
            f"  - Votes: {self.vote_count}\n"
            f"  - Up Votes: {self.up_count}"
        )

class Creator(BaseModelWithArbitraryTypes):
    address: str
    percentage: int

class CollectionOptions(BaseModelWithArbitraryTypes):
    name: str
    uri: str
    royalty_basis_points: Optional[int] = None
    creators: Optional[List[Creator]] = None

class CollectionDeployment(BaseModelWithArbitraryTypes):
    collection_address: Pubkey
    signature: bytes

class MintCollectionNFTResponse(BaseModelWithArbitraryTypes):
    mint: Pubkey
    metadata: Pubkey

class PumpfunTokenOptions(BaseModelWithArbitraryTypes):
    twitter: Optional[str] = None
    telegram: Optional[str] = None
    website: Optional[str] = None
    initial_liquidity_sol: Optional[float] = None
    slippage_bps: Optional[int] = None
    priority_fee: Optional[int] = None

class PumpfunLaunchResponse(BaseModelWithArbitraryTypes):
    signature: str
    mint: str
    metadata_uri: Optional[str] = None
    error: Optional[str] = None

class LuloAccountSettings(BaseModelWithArbitraryTypes):
    owner: str
    allowed_protocols: Optional[str] = None
    homebase: Optional[str] = None
    minimum_rate: str

class LuloAccountDetailsResponse(BaseModelWithArbitraryTypes):
    total_value: float
    interest_earned: float
    realtime_apy: float
    settings: LuloAccountSettings

class NetworkPerformanceMetrics(BaseModelWithArbitraryTypes):
    """Data structure for Solana network performance metrics."""
    transactions_per_second: float
    total_transactions: int
    sampling_period_seconds: int
    current_slot: int

class TokenDeploymentResult(BaseModelWithArbitraryTypes):
    """Result of a token deployment operation."""
    mint: Pubkey
    transaction_signature: str

class TokenLaunchResult(BaseModelWithArbitraryTypes):
    """Result of a token launch operation."""
    signature: str
    mint: str
    metadata_uri: str

class TransferResult(BaseModelWithArbitraryTypes):
    """Result of a transfer operation."""
    signature: str
    from_address: str
    to_address: str
    amount: float
    token: Optional[str] = None

class JupiterTokenData(BaseModelWithArbitraryTypes):
    address:str
    symbol:str
    name:str

class GibworkCreateTaskResponse(BaseModelWithArbitraryTypes):
    status: str
    taskId: Optional[str] = None
    signature: Optional[str] = None

class BondingCurveState:
    _STRUCT = Struct(
        "virtual_token_reserves" / Int64ul,
        "virtual_sol_reserves" / Int64ul,
        "real_token_reserves" / Int64ul,
        "real_sol_reserves" / Int64ul,
        "token_total_supply" / Int64ul,
        "complete" / Flag
    )
    def __init__(self, data: bytes) -> None:
        parsed = self._STRUCT.parse(data[8:])