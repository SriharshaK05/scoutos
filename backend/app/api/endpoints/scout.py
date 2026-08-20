from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.scout import ScoutRequest, ScoutResult
from app.services.scout import search_players

router = APIRouter()

@router.post("/search", response_model=List[ScoutResult])
def scout_search(criteria: ScoutRequest, db: Session = Depends(get_db)):
    """Search for players based on demographic and statistical criteria."""
    return search_players(db, criteria)