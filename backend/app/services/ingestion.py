from sqlalchemy.orm import Session
from app.models.player import Player, Team, PlayerSeason
from app.schemas.ingestion import RawPlayer

def ingest_players(db: Session, raw_players: list[RawPlayer]):
    stats = {"players_created": 0, "teams_created": 0, "seasons_created": 0}
    
    for raw_player in raw_players:
        # 1. Player Deduplication
        player = db.query(Player).filter(Player.name == raw_player.name).first()
        if not player:
            player = Player(
                name=raw_player.name,
                position=raw_player.position,
                height_inches=raw_player.height_inches,
                weight_lbs=raw_player.weight_lbs,
                birth_date=raw_player.birth_date
            )
            db.add(player)
            db.flush() # Gets the new ID without fully committing yet
            stats["players_created"] += 1
        
        # 2. Process Teams and Seasons
        for raw_season in raw_player.seasons:
            # Team Deduplication
            team = db.query(Team).filter(Team.abbreviation == raw_season.team_abbreviation).first()
            if not team:
                team = Team(
                    abbreviation=raw_season.team_abbreviation,
                    city=raw_season.team_city,
                    name=raw_season.team_name
                )
                db.add(team)
                db.flush()
                stats["teams_created"] += 1
            
            # Season Deduplication
            season_record = db.query(PlayerSeason).filter(
                PlayerSeason.player_id == player.id,
                PlayerSeason.team_id == team.id,
                PlayerSeason.season == raw_season.season
            ).first()
            
            if not season_record:
                season_record = PlayerSeason(
                    player_id=player.id,
                    team_id=team.id,
                    season=raw_season.season,
                    games_played=raw_season.games_played,
                    minutes_played=raw_season.minutes_played,
                    points=raw_season.points,
                    assists=raw_season.assists,
                    rebounds=raw_season.rebounds
                )
                db.add(season_record)
                stats["seasons_created"] += 1
    
    # Commit all changes as a single transaction
    db.commit()
    return stats