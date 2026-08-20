from pydantic import BaseModel
from typing import List, Optional

class ScoutRequest(BaseModel):
    positions: Optional[List[str]] = None
    min_mpg: Optional[float] = None
    min_ppg: Optional[float] = None
    min_apg: Optional[float] = None
    min_rpg: Optional[float] = None

class ScoutResult(BaseModel):
    player_id: int
    name: str
    position: str
    season: str
    team: str
    mpg: float
    ppg: float
    apg: float
    rpg: float