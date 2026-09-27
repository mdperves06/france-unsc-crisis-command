import sys
import pytest
sys.path.insert(0, 'backend')
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_unsc_members_and_presidency(client):
    res = client.get("/api/v1/unsc/members?year=2026")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 5 # P5
    # Verify France has veto
    france = next((m for m in data if m["country_code"] == "FRA"), None)
    assert france is not None
    assert france["has_veto"] is True

    # Check presidencies
    p_res = client.get("/api/v1/unsc/presidencies?year=2026")
    assert p_res.status_code == 200
    p_data = p_res.json()
    assert len(p_data) > 0

def test_unsc_resolutions_and_votes(client):
    res = client.get("/api/v1/unsc/resolutions")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 3 # S/RES/2728, 2722, 1701

    votes_res = client.get("/api/v1/unsc/votes")
    assert votes_res.status_code == 200
    
    vetoes_res = client.get("/api/v1/unsc/vetoes")
    assert vetoes_res.status_code == 200
    vetoes = vetoes_res.json()
    assert any(v["is_veto"] for v in vetoes)
