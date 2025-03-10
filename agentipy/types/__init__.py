
from typing import Dict, List, Optional

from construct import Flag, Int64ul, Struct
from pydantic import BaseModel
from solders.pubkey import Pubkey  # type: ignore


class BaseModelWithArbitraryTypes(BaseModel):
    class Config:
        arbitrary_types_allowed = True

class TokenCheck(BaseModelWithArbitraryTypes):
    token_program:str
    token_type: str
    risks: Optional[List[Dict]] = None 
    score: int
    
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

class TokenCheck(BaseModelWithArbitraryTypes):
    token_program:str
    token_type: str
    risks: List[Dict]
    score: int

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
        self.__dict__.update(parsed)
