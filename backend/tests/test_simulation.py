import sys
import pytest

def test_full_practice_arena_flow(client):
    # 1. Fetch benchmark scenario
    res = client.get("/api/v1/intelligence/regions")
    assert res.status_code == 200
    
    # Generate or get scenario
    scen_res = client.post("/api/v1/crisis/generate", json={
        "region": "Middle East",
        "crisis_type": "Diplomatic & Border Security",
        "difficulty": "Intermediate"
    })
    assert scen_res.status_code == 200
    scen_id = scen_res.json()["scenario_id"]

    # 2. Start Practice Arena session
    start_res = client.post("/api/v1/practice/start", json={
        "scenario_id": scen_id,
        "difficulty": "Intermediate",
        "year": 2026
    })
    assert start_res.status_code == 200
    session_id = start_res.json()["session_id"]
    assert session_id.startswith("sim-")

    # 3. Check Initial World State
    state_res = client.get(f"/api/v1/practice/{session_id}/world-state")
    assert state_res.status_code == 200
    state = state_res.json()
    assert state["turn"] == 1
    assert "FRA" in state["coalition_status"]["support"]

    # 4. France takes action: Contact USA
    act_res = client.post("/api/v1/practice/action", json={
        "session_id": session_id,
        "action_type": "CONTACT_USA",
        "target_country": "USA",
        "parameters": {"proposal": "Coordinate joint P3 draft resolution"}
    })
    assert act_res.status_code == 200
    act_data = act_res.json()
    assert act_data["updated_world_state"]["turn"] == 2

    # 5. Check Messages
    msg_res = client.get(f"/api/v1/practice/{session_id}/messages")
    assert msg_res.status_code == 200
    messages = msg_res.json()
    assert len(messages) >= 2 # Initial cable + Turn 2 reply

    # 6. Check Timeline
    time_res = client.get(f"/api/v1/practice/{session_id}/timeline")
    assert time_res.status_code == 200
    assert len(time_res.json()) >= 1

    # 7. Create What-If Branch
    whatif_res = client.post("/api/v1/practice/what-if", json={
        "source_session_id": session_id,
        "target_turn": 1,
        "alternative_action_type": "CONTACT_CHINA"
    })
    assert whatif_res.status_code == 200
    assert whatif_res.json()["branch_session_id"].startswith("branch-")

    # 8. Trigger After-Action Review (AAR)
    aar_res = client.post(f"/api/v1/practice/{session_id}/aar")
    assert aar_res.status_code == 200
    aar_data = aar_res.json()
    assert "what_user_did" in aar_data
    assert "full_analysis" in aar_data

def test_training_and_labs_endpoints(client):
    # 1. Panic Button ("I Don't Know What To Do")
    panic_res = client.post("/api/v1/crisis/panic?scenario_id=none")
    assert panic_res.status_code == 200
    panic_data = panic_res.json()
    assert len(panic_data["three_strategic_paths"]) == 3

    # 2. Speech Analysis Lab
    speech_res = client.post("/api/v1/training/speech/analyze", json={
        "speech_type": "CRISIS_SPEECH",
        "speech_text": "Mr. President, France calls upon all members of this Council to enforce immediate humanitarian access in accordance with Article 24 and international humanitarian law."
    })
    assert speech_res.status_code == 200
    assert speech_res.json()["overall_score"] > 6.0

    # 3. Resolution Lab Validation
    res_val = client.post("/api/v1/training/resolution/validate", json={
        "title": "Draft Resolution on Humanitarian Corridors",
        "preambulatory_clauses": ["Recalling S/RES/1701 (2006) and S/RES/2728 (2024)"],
        "operative_clauses": [
            "Demands the immediate opening of unhindered humanitarian corridors",
            "Requests the Secretary-General deploy a neutral civilian observer mission"
        ]
    })
    assert res_val.status_code == 200
    assert res_val.json()["voting_viability_score"] >= 80.0

    # 4. EB Attack Simulator
    eb_res = client.post("/api/v1/training/eb/question", json={
        "scenario_context": "Peacekeeping buffer deployment under Chapter VI",
        "france_stated_position": "France advocates immediate UN buffer monitoring"
    })
    assert eb_res.status_code == 200
    assert len(eb_res.json()["question"]) > 10


def test_practice_unknown_session_returns_404(client):
    assert client.post("/api/v1/practice/action", json={
        "session_id": "missing", "action_type": "CONTACT_CHINA", "target_country": "CHN", "parameters": {}, "rationale": ""
    }).status_code == 404
    assert client.post("/api/v1/practice/negotiate", json={
        "session_id": "missing", "recipient_country": "CHN", "content": "hello"
    }).status_code == 404
    assert client.post("/api/v1/practice/what-if", json={
        "source_session_id": "missing", "target_turn": 1, "alternative_action_type": "PROPOSE_CEASEFIRE"
    }).status_code == 404


def test_practice_world_state_carries_over_between_turns(client):
    # Unknown scenario id (the frontend default) falls back to a real scenario
    session_id = client.post("/api/v1/practice/start", json={"scenario_id": "scenario-default"}).json()["session_id"]
    before = client.get(f"/api/v1/practice/{session_id}/world-state").json()

    res = client.post("/api/v1/practice/action", json={
        "session_id": session_id, "action_type": "CONTACT_CHINA", "target_country": "CHN", "parameters": {}, "rationale": "Consult Beijing"
    })
    assert res.status_code == 200
    vote = res.json()["updated_world_state"]["projected_vote"]
    assert vote["yes_estimate"] + vote["no_estimate"] + vote["abstain_estimate"] == 15

    after = client.get(f"/api/v1/practice/{session_id}/world-state").json()
    assert after["turn"] == before["turn"] + 1
    for field in ["france_credibility", "humanitarian_status", "economic_status"]:
        assert after[field] == before[field]


def test_research_upload_indexes_whole_document(client):
    # 30k chars -> ~38 chunks; text near the end must still be searchable
    body = ("Background on the Security Council. " * 800) + "UNIQUEMARKERXYZ closing annex."
    res = client.post(
        "/api/v1/research/upload",
        files={"file": ("NOTES.TXT", body.encode(), "text/plain")},
        data={"title": "Long briefing"},
    )
    assert res.status_code == 200 and res.json()["chunks"] > 20
    hits = client.get("/api/v1/research/search", params={"query": "UNIQUEMARKERXYZ"}).json()
    assert any(h["document_title"] == "Long briefing" for h in hits)
