from pydantic import BaseModel
from typing import List
from datetime import date

class RawPlayerSeason(BaseModel):
    team_abbreviation: str
    team_city: str
    team_name: str
    season: str
    games_played: int = 0
    minutes_played: int = 0
    points: int = 0
    assists: int = 0
    rebounds: int = 0

class RawPlayer(BaseModel):
    name: str
    position: str
    height_inches: int
    weight_lbs: int
    birth_date: date
    seasons: List[RawPlayerSeason] = []

class IngestionPayload(BaseModel):
    players: List[RawPlayer]