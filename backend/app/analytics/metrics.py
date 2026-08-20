def calculate_per_game_metrics(games: int, minutes: int, points: int, assists: int, rebounds: int) -> dict:
    """Calculates per-game averages safely."""
    if games == 0:
        return {"mpg": 0.0, "ppg": 0.0, "apg": 0.0, "rpg": 0.0}
    
    return {
        "mpg": round(minutes / games, 1),
        "ppg": round(points / games, 1),
        "apg": round(assists / games, 1),
        "rpg": round(rebounds / games, 1),
    }