import os
import sys
import tempfile
from pathlib import Path

import pytest

# Isolate tests before the app is imported: throwaway DB, no cloud AI calls (offline fallbacks)
_tmp_dir = tempfile.mkdtemp(prefix="unsc_tests_")
os.environ["DATABASE_URL"] = f"sqlite:///{Path(_tmp_dir, 'test.db').as_posix()}"
for _key in ("GEMINI_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
    os.environ[_key] = ""
os.environ["LOCAL_AI_BASE_URL"] = "http://127.0.0.1:9"  # unreachable -> instant local fallback

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402

ADMIN_EMAIL = "admin@france-unsc.org"
ADMIN_PASSWORD = "admin123"


@pytest.fixture
def anon_client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def client(anon_client):
    res = anon_client.post("/api/v1/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert res.status_code == 200, res.text
    anon_client.headers["Authorization"] = f"Bearer {res.json()['access_token']}"
    return anon_client
