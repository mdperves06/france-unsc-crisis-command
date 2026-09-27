import uuid

from app.services.auth_service import _hash_password, _verify_password, _pbkdf2, _LEGACY_SALT


def _new_user(**overrides):
    u = uuid.uuid4().hex[:8]
    payload = {"email": f"u{u}@test.org", "username": f"u{u}", "full_name": "Test User", "password": "correct-horse"}
    payload.update(overrides)
    return payload


def test_protected_endpoints_require_login(anon_client):
    for path in ["/api/v1/unsc/members", "/api/v1/intelligence/regions", "/api/v1/training/curriculum"]:
        assert anon_client.get(path).status_code == 401
    assert anon_client.post("/api/v1/chat", json={"prompt": "hi"}).status_code == 401
    assert anon_client.get("/api/v1/unsc/members", headers={"Authorization": "Bearer forged.token"}).status_code == 401


def test_register_login_and_me(anon_client):
    payload = _new_user()
    res = anon_client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 200
    assert res.json()["user"]["role"] == "student"

    res = anon_client.post("/api/v1/auth/login", json={"email": payload["email"], "password": payload["password"]})
    assert res.status_code == 200
    token = res.json()["access_token"]
    me = anon_client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200 and me.json()["email"] == payload["email"]

    wrong = anon_client.post("/api/v1/auth/login", json={"email": payload["email"], "password": "not-the-password"})
    assert wrong.status_code == 401


def test_register_cannot_self_assign_privileged_role(anon_client):
    for role in ["admin", "coach"]:
        res = anon_client.post("/api/v1/auth/register", json=_new_user(role=role))
        assert res.status_code == 400
    assert anon_client.post("/api/v1/auth/register", json=_new_user(role="delegate")).status_code == 200


def test_register_rejects_short_password(anon_client):
    assert anon_client.post("/api/v1/auth/register", json=_new_user(password="short")).status_code == 422


def test_password_hashes_are_salted_and_legacy_hashes_verify():
    a, b = _hash_password("same-password"), _hash_password("same-password")
    assert a != b
    assert _verify_password("same-password", a) and not _verify_password("other", a)
    legacy = _pbkdf2("old-password", _LEGACY_SALT)
    assert _verify_password("old-password", legacy)
