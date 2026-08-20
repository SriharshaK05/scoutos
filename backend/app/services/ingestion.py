from sqlalchemy.orm import Session
from app.models.player import Player, Team, PlayerSeason, PlayerFeature # <-- Add PlayerFeature
from app.schemas.ingestion import RawPlayer
from app.analytics.metrics import calculate_per_game_metrics # <-- Add this

def ingest_players(db: Session, raw_players: list[RawPlayer]):
    stats = {"players_created": 0, "teams_created": 0, "seasons_created": 0, "features_generated": 0} # <-- Update stats dict
    
    for raw_player in raw_players:
        # 1. Player Deduplication
        player = db.query(Player).filter(Player.name == raw_player.name).first()
        if not player:
            player = Player(
                name=raw_player.name, position=raw_player.position,
                height_inches=raw_player.height_inches, weight_lbs=raw_player.weight_lbs,
                birth_date=raw_player.birth_date
            )
            db.add(player)
            db.flush()
            stats["players_created"] += 1
        
        # 2. Process Teams and Seasons
        for raw_season in raw_player.seasons:
            team = db.query(Team).filter(Team.abbreviation == raw_season.team_abbreviation).first()
            if not team:
                team = Team(abbreviation=raw_season.team_abbreviation, city=raw_season.team_city, name=raw_season.team_name)
                db.add(team)
                db.flush()
                stats["teams_created"] += 1
            
            season_record = db.query(PlayerSeason).filter(
                PlayerSeason.player_id == player.id, PlayerSeason.team_id == team.id, PlayerSeason.season == raw_season.season
            ).first()
            
            if not season_record:
                season_record = PlayerSeason(
                    player_id=player.id, team_id=team.id, season=raw_season.season,
                    games_played=raw_season.games_played, minutes_played=raw_season.minutes_played,
                    points=raw_season.points, assists=raw_season.assists, rebounds=raw_season.rebounds
                )
                db.add(season_record)
                db.flush() # Need this to get the season_record.id for the features table
                stats["seasons_created"] += 1

                # 3. GENERATE FEATURES (New Code Block)
                calculated_metrics = calculate_per_game_metrics(
                    games=season_record.games_played, minutes=season_record.minutes_played,
                    points=season_record.points, assists=season_record.assists, rebounds=season_record.rebounds
                )
                
                features = PlayerFeature(
                    player_season_id=season_record.id,
                    mpg=calculated_metrics["mpg"],
                    ppg=calculated_metrics["ppg"],
                    apg=calculated_metrics["apg"],
                    rpg=calculated_metrics["rpg"]
                )
                db.add(features)
                stats["features_generated"] += 1
                
    db.commit()
    return stats