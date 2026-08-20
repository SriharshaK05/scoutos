from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.endpoints import data  # <-- ADD THIS

app = FastAPI(title="SCOUTOS API", description="Intelligent Sports Scouting Platform")

app.include_router(data.router, prefix="/api/data", tags=["data"])

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
        
    return {
        "status": "ok",
        "database": db_status
    }