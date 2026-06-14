from flask import Flask, jsonify, request
from datetime import datetime
from collections import defaultdict
import time, os, platform, psutil

app = Flask(__name__)

# ── In-memory storage ─────────────────────────────
TASKS = {}
START_TIME = time.time()
REQUEST_COUNTS = defaultdict(int)
ERROR_COUNTS = defaultdict(int)

APP_VERSION = os.getenv("APP_VERSION", "2.0.0")


# ── Helper ────────────────────────────────────────
def track(name):
    REQUEST_COUNTS[name] += 1


# ══════════════════════════════════════════════════
# HEALTH & INFO
# ══════════════════════════════════════════════════

@app.route("/")
def home():
    track("home")
    return jsonify({
        "app":     "Flask Task Manager API",
        "version": APP_VERSION,
        "status":  "running",
        "endpoints": [
            "GET  /health",
            "GET  /api/info",
            "GET  /api/stats",
            "GET  /api/tasks",
            "POST /api/tasks",
            "GET  /api/tasks/<id>",
            "PATCH /api/tasks/<id>",
            "DELETE /api/tasks/<id>",
            "GET  /metrics"
        ]
    })


@app.route("/health")
def health():
    track("health")
    uptime = round(time.time() - START_TIME)
    return jsonify({
        "status":        "healthy",
        "version":       APP_VERSION,
        "uptime_seconds": uptime,
        "uptime_human":  f"{uptime // 3600}h {(uptime % 3600) // 60}m {uptime % 60}s",
        "timestamp":     datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route("/api/info")
def info():
    track("info")
    return jsonify({
        "app":      "Flask Task Manager API",
        "version":  APP_VERSION,
        "python":   platform.python_version(),
        "platform": platform.system(),
        "hostname": platform.node(),
        "pid":      os.getpid()
    }), 200


@app.route("/api/stats")
def stats():
    track("stats")
    mem  = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return jsonify({
        "system": {
            "cpu_percent":    psutil.cpu_percent(interval=0.5),
            "memory_percent": mem.percent,
            "memory_used_mb": round(mem.used / 1024**2, 1),
            "memory_total_mb": round(mem.total / 1024**2, 1),
            "disk_percent":   disk.percent,
            "disk_used_gb":   round(disk.used / 1024**3, 2),
        },
        "application": {
            "total_tasks":   len(TASKS),
            "done_tasks":    sum(1 for t in TASKS.values() if t["status"] == "done"),
            "pending_tasks": sum(1 for t in TASKS.values() if t["status"] == "pending"),
            "request_counts": dict(REQUEST_COUNTS),
            "error_counts":   dict(ERROR_COUNTS),
        }
    }), 200


# ══════════════════════════════════════════════════
# TASK CRUD
# ══════════════════════════════════════════════════

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    track("get_tasks")
    status_f   = request.args.get("status")
    priority_f = request.args.get("priority")

    tasks = list(TASKS.values())
    if status_f:
        tasks = [t for t in tasks if t["status"] == status_f]
    if priority_f:
        tasks = [t for t in tasks if t["priority"] == priority_f]

    return jsonify({"tasks": tasks, "total": len(tasks)}), 200


@app.route("/api/tasks", methods=["POST"])
def create_task():
    track("create_task")
    data = request.get_json(silent=True)
    if not data:
        ERROR_COUNTS["bad_request"] += 1
        return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get("title", "").strip()
    if not title:
        ERROR_COUNTS["validation_error"] += 1
        return jsonify({"error": "title is required"}), 422

    status   = data.get("status", "pending")
    priority = data.get("priority", "medium")

    if status not in ("pending", "in_progress", "done"):
        return jsonify({"error": "status must be pending, in_progress, or done"}), 422
    if priority not in ("low", "medium", "high"):
        return jsonify({"error": "priority must be low, medium, or high"}), 422

    import uuid
    task_id = str(uuid.uuid4())[:8]
    task = {
        "id":          task_id,
        "title":       title,
        "description": data.get("description", "").strip(),
        "status":      status,
        "priority":    priority,
        "created_at":  datetime.utcnow().isoformat() + "Z",
        "updated_at":  None
    }
    TASKS[task_id] = task
    return jsonify({"message": "Task created", "task": task}), 201


@app.route("/api/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    track("get_task")
    task = TASKS.get(task_id)
    if not task:
        ERROR_COUNTS["not_found"] += 1
        return jsonify({"error": f"Task '{task_id}' not found"}), 404
    return jsonify(task), 200


@app.route("/api/tasks/<task_id>", methods=["PATCH"])
def update_task(task_id):
    track("update_task")
    task = TASKS.get(task_id)
    if not task:
        return jsonify({"error": f"Task '{task_id}' not found"}), 404

    data = request.get_json(silent=True) or {}
    if "status" in data:
        if data["status"] not in ("pending", "in_progress", "done"):
            return jsonify({"error": "Invalid status"}), 422
        task["status"] = data["status"]
    if "priority" in data:
        task["priority"] = data["priority"]
    if "description" in data:
        task["description"] = data["description"]

    task["updated_at"] = datetime.utcnow().isoformat() + "Z"
    TASKS[task_id] = task
    return jsonify({"message": "Task updated", "task": task}), 200


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    track("delete_task")
    if task_id not in TASKS:
        return jsonify({"error": f"Task '{task_id}' not found"}), 404
    del TASKS[task_id]
    return jsonify({"message": f"Task '{task_id}' deleted"}), 200


# ══════════════════════════════════════════════════
# PROMETHEUS METRICS
# ══════════════════════════════════════════════════

@app.route("/metrics")
def metrics():
    track("metrics")
    lines = [
        "# HELP app_tasks_total Total tasks in memory",
        "# TYPE app_tasks_total gauge",
        f"app_tasks_total {len(TASKS)}",
        "",
        "# HELP app_uptime_seconds App uptime in seconds",
        "# TYPE app_uptime_seconds counter",
        f"app_uptime_seconds {round(time.time() - START_TIME)}",
        "",
        "# HELP app_requests_total Requests per endpoint",
        "# TYPE app_requests_total counter",
    ]
    for ep, count in REQUEST_COUNTS.items():
        lines.append(f'app_requests_total{{endpoint="{ep}"}} {count}')
    return "\n".join(lines) + "\n", 200, {"Content-Type": "text/plain"}


# ══════════════════════════════════════════════════
# ERROR HANDLERS
# ══════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    ERROR_COUNTS["404"] += 1
    return jsonify({"error": "Endpoint not found", "path": request.path}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    ERROR_COUNTS["405"] += 1
    return jsonify({"error": "Method not allowed"}), 405


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
