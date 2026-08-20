from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.endpoints import data, players, scout

app = FastAPI(title="SCOUTOS API", description="Intelligent Sports Scouting Platform")

app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(players.router, prefix="/api/players", tags=["players"])
app.include_router(scout.router, prefix="/api/scout", tags=["scout"])

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