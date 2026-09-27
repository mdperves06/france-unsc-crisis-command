def _play(client, moves):
    session_id = client.post("/api/v1/practice/start", json={"scenario_id": "scenario-default"}).json()["session_id"]
    outcomes = []
    for action_type, target in moves:
        res = client.post("/api/v1/practice/action", json={
            "session_id": session_id, "action_type": action_type, "target_country": target, "parameters": {}, "rationale": ""
        })
        assert res.status_code == 200
        vote = res.json()["updated_world_state"]["projected_vote"]
        assert vote["yes_estimate"] + vote["no_estimate"] + vote["abstain_estimate"] == 15
        outcomes.append((vote["yes_estimate"], vote["outcome_prediction"]))
    return outcomes


GOOD_STRATEGY = [
    ("REQUEST_EMERGENCY_MEETING", "USA"),
    ("PROPOSE_CEASEFIRE", "SOM"),
    ("CONSULT_A3", "COD"),
    ("CONTACT_CHINA", "CHN"),
    ("CONTACT_RUSSIA", "RUS"),
]


def test_good_strategy_can_pass_but_not_instantly(client):
    outcomes = _play(client, GOOD_STRATEGY)
    print(outcomes)
    assert outcomes[-1][1] == "WOULD PASS"
    assert outcomes[0][1] != "WOULD PASS"


def test_spamming_one_action_has_diminishing_returns(client):
    outcomes = _play(client, [("PROPOSE_CEASEFIRE", "SOM")] * 3)
    print(outcomes)
    assert all(o[1] != "WOULD PASS" for o in outcomes)


def test_escalation_never_passes(client):
    outcomes = _play(client, [("THREATEN_VETO", "RUS"), ("DEMAND_SANCTIONS", "RUS"), ("UNILATERAL_STATEMENT", "USA")])
    print(outcomes)
    assert all(o[1] != "WOULD PASS" for o in outcomes)
