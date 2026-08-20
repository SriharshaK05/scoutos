from sqlalchemy.orm import Session
from app.models.player import Player, PlayerSeason, PlayerFeature, Team
from app.schemas.scout import ScoutRequest

def search_players(db: Session, criteria: ScoutRequest):
    # 1. Base Query: Join all relevant tables
    query = db.query(
        Player.id.label("player_id"),
        Player.name,
        Player.position,
        PlayerSeason.season,
        Team.abbreviation.label("team"),
        PlayerFeature.mpg,
        PlayerFeature.ppg,
        PlayerFeature.apg,
        PlayerFeature.rpg
    ).join(PlayerSeason, Player.id == PlayerSeason.player_id)\
     .join(Team, PlayerSeason.team_id == Team.id)\
     .join(PlayerFeature, PlayerSeason.id == PlayerFeature.player_season_id)

    # 2. Dynamic Filtering: Only filter on criteria the caller provided
    if criteria.positions:
        query = query.filter(Player.position.in_(criteria.positions))
    if criteria.min_mpg is not None:
        query = query.filter(PlayerFeature.mpg >= criteria.min_mpg)
    if criteria.min_ppg is not None:
        query = query.filter(PlayerFeature.ppg >= criteria.min_ppg)
    if criteria.min_apg is not None:
        query = query.filter(PlayerFeature.apg >= criteria.min_apg)
    if criteria.min_rpg is not None:
        query = query.filter(PlayerFeature.rpg >= criteria.min_rpg)

    # 3. Execute query and format records
    results = query.all()
    
    return [
        {
            "player_id": r.player_id,
            "name": r.name,
            "position": r.position,
            "season": r.season,
            "team": r.team,
            "mpg": r.mpg,
            "ppg": r.ppg,
            "apg": r.apg,
            "rpg": r.rpg
        }
        for r in results
    ]