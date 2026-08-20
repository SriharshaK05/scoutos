from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.player import Player

router = APIRouter()

@router.get("/{player_id}/stats")
def get_player_stats(player_id: int, db: Session = Depends(get_db)):
    """Retrieve a player and their calculated season features."""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    seasons_data = []
    for season in player.seasons:
        feature = season.features[0] if season.features else None
        seasons_data.append({
            "season": season.season,
            "team": season.team.abbreviation,
            "mpg": feature.mpg if feature else 0.0,
            "ppg": feature.ppg if feature else 0.0,
            "apg": feature.apg if feature else 0.0,
            "rpg": feature.rpg if feature else 0.0,
        })
        
    return {
        "id": player.id,
        "name": player.name,
        "stats": seasons_data
    }