import pytest, json
from app import app, TASKS

@pytest.fixture(autouse=True)
def clear():
    TASKS.clear()
    yield
    TASKS.clear()

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def post_task(client, title="Fix pipeline", priority="high"):
    return client.post("/api/tasks",
        data=json.dumps({"title": title, "priority": priority}),
        content_type="application/json")

# ── Health ─────────────────────────────────────────
def test_health_200(client):
    assert client.get("/health").status_code == 200

def test_health_status_field(client):
    assert client.get("/health").get_json()["status"] == "healthy"

def test_health_has_uptime(client):
    assert "uptime_seconds" in client.get("/health").get_json()

def test_home_returns_endpoints(client):
    data = client.get("/").get_json()
    assert "endpoints" in data

def test_info_endpoint(client):
    r = client.get("/api/info").get_json()
    assert "python" in r and "version" in r

def test_stats_endpoint(client):
    r = client.get("/api/stats").get_json()
    assert "system" in r
    assert "cpu_percent" in r["system"]

# ── Tasks ──────────────────────────────────────────
def test_get_tasks_empty(client):
    r = client.get("/api/tasks").get_json()
    assert r["total"] == 0

def test_create_task(client):
    r = post_task(client, "Deploy to prod")
    assert r.status_code == 201
    assert r.get_json()["task"]["title"] == "Deploy to prod"

def test_create_task_no_title(client):
    r = client.post("/api/tasks",
        data=json.dumps({"priority": "high"}),
        content_type="application/json")
    assert r.status_code == 422

def test_create_task_bad_status(client):
    r = client.post("/api/tasks",
        data=json.dumps({"title": "test", "status": "invalid"}),
        content_type="application/json")
    assert r.status_code == 422

def test_get_task_by_id(client):
    task_id = post_task(client).get_json()["task"]["id"]
    assert client.get(f"/api/tasks/{task_id}").status_code == 200

def test_get_task_not_found(client):
    assert client.get("/api/tasks/abc99999").status_code == 404

def test_update_task(client):
    task_id = post_task(client).get_json()["task"]["id"]
    r = client.patch(f"/api/tasks/{task_id}",
        data=json.dumps({"status": "done"}),
        content_type="application/json")
    assert r.status_code == 200
    assert r.get_json()["task"]["status"] == "done"

def test_delete_task(client):
    task_id = post_task(client).get_json()["task"]["id"]
    assert client.delete(f"/api/tasks/{task_id}").status_code == 200
    assert client.get(f"/api/tasks/{task_id}").status_code == 404

def test_filter_by_status(client):
    post_task(client, "task1")
    tid = post_task(client, "task2").get_json()["task"]["id"]
    client.patch(f"/api/tasks/{tid}",
        data=json.dumps({"status": "done"}),
        content_type="application/json")
    r = client.get("/api/tasks?status=done").get_json()
    assert r["total"] == 1

# ── Metrics ────────────────────────────────────────
def test_metrics_endpoint(client):
    r = client.get("/metrics")
    assert r.status_code == 200
    assert b"app_tasks_total" in r.data
