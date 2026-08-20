from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ingestion import IngestionPayload
from app.services.ingestion import ingest_players

router = APIRouter()

@router.post("/upload")
def upload_data(payload: IngestionPayload, db: Session = Depends(get_db)):
    """Ingest a batch of raw player data."""
    stats = ingest_players(db, payload.players)
    return {"status": "success", "stats": stats}