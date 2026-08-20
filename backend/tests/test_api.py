from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"


import uuid

def test_data_ingestion_idempotency():
    # 1. Create a unique player and unique team per test run
    unique_id = str(uuid.uuid4())[:6]
    unique_name = f"Test Player {unique_id}"
    unique_team = unique_id[:3].upper()

    payload = {
        "players": [
            {
                "name": unique_name,
                "position": "PG",
                "height_inches": 74,
                "weight_lbs": 190,
                "birth_date": "1999-01-01",
                "seasons": [
                    {
                        "team_abbreviation": unique_team,
                        "team_city": "Test City",
                        "team_name": "Testers",
                        "season": "2023-24",
                        "games_played": 10,
                        "minutes_played": 200,
                        "points": 150,
                        "assists": 50,
                        "rebounds": 30
                    }
                ]
            }
        ]
    }

    # 2. First upload - should successfully create player and team
    response1 = client.post("/api/data/upload", json=payload)
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["stats"]["players_created"] == 1
    assert data1["stats"]["teams_created"] == 1
    assert data1["stats"]["seasons_created"] == 1

    # 3. Second upload (idempotency check) - should create 0 records
    response2 = client.post("/api/data/upload", json=payload)
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["stats"]["players_created"] == 0
    assert data2["stats"]["teams_created"] == 0
    assert data2["stats"]["seasons_created"] == 0

def test_scout_search_filters():
    # 1. Search for an impossibly high PPG to verify empty results
    response = client.post("/api/scout/search", json={"min_ppg": 99.0})
    assert response.status_code == 200
    assert response.json() == []

    # 2. Search with empty criteria to verify all players with features return
    response_all = client.post("/api/scout/search", json={})
    assert response_all.status_code == 200
    assert isinstance(response_all.json(), list)