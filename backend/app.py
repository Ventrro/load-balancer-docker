from flask import Flask, jsonify
import os
import socket
from datetime import datetime, timezone

app = Flask(__name__)

def get_instance_name() -> str:
    # Prefer explicit env var you control
    return (
        os.getenv("INSTANCE_NAME")
        or os.getenv("CONTAINER_NAME")
        or socket.gethostname()
        or "unknown"
    )

def get_container_id_short() -> str:
    """
    Best-effort: extract container ID from cgroup info (works in Linux containers).
    Returns 'unknown' if not available (e.g., non-Linux or different runtime).
    """
    cgroup_paths = ["/proc/self/cgroup", "/proc/1/cgroup"]
    for path in cgroup_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    # Docker/containerd IDs are typically 64 hex chars
                    parts = line.strip().split("/")
                    for p in reversed(parts):
                        if len(p) >= 12 and all(ch in "0123456789abcdef" for ch in p[:12].lower()):
                            return p[:12]
        except OSError:
            continue
    return "unknown"

def base_payload():
    return {
        "service": os.getenv("SERVICE_NAME", "backend"),
        "instance": get_instance_name(),
        "hostname": socket.gethostname(),
        "container_id": get_container_id_short(),
        "status": "running",
        "time_utc": datetime.now(timezone.utc).isoformat(),
    }

@app.route("/", methods=["GET"])
def home():
    data = base_payload()
    data["message"] = "Hello from backend!"
    data["endpoints"] = {
        "health": "/health",
        "whoami": "/whoami",
    }
    return jsonify(data), 200

@app.route("/whoami", methods=["GET"])
def whoami():
    return jsonify(base_payload()), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    # Keep host/port configurable but default to 5000
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    app.run(host=host, port=port)
