import os
import threading
from collections import deque
from datetime import datetime

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
ATOM_API_KEY = os.getenv("ATOM_API_KEY")
if not ATOM_API_KEY:
    raise RuntimeError("ATOM_API_KEY is not configured")

JOB_TTL_SECONDS = 30
ONLINE_TIMEOUT_SECONDS = 10
ALLOWED_JOBS = ["letter", "show_image"]
ALLOWED_IMAGES = ("smile", "heart", "checker")
FINAL_RESULTS = ("done", "refused", "error", "expired")

# Unclaimed jobs are FIFO; dispatched jobs retain their individual status.
pending_jobs = deque()
jobs = {}
state_lock = threading.Lock()
last_job = None
last_seen = None
next_job_id = 1


def expire_pending_jobs():
    # Caller holds state_lock. Only unclaimed jobs expire.
    now = datetime.now()
    remaining = deque()
    while pending_jobs:
        job_id = pending_jobs.popleft()
        job = jobs[job_id]
        if (now - job["created_at"]).total_seconds() >= JOB_TTL_SECONDS:
            job["status"] = "expired"
        else:
            remaining.append(job_id)
    pending_jobs.extend(remaining)


def public_job(job):
    return {key: job[key] for key in ("id", "job", "arg", "status")}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/jobs", methods=["POST"])
def create_job():
    global last_job, next_job_id
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(status="refused", reason="JSON object required"), 400
    job_type, argument = data.get("job"), data.get("arg")
    if job_type not in ALLOWED_JOBS:
        return jsonify(status="refused", reason="Unknown or forbidden job"), 400
    if job_type == "letter":
        if (not isinstance(argument, str) or len(argument) != 1
                or len(argument.upper()) != 1 or not "A" <= argument.upper() <= "Z"):
            return jsonify(status="refused", reason="Letter must be A-Z"), 400
        argument = argument.upper()
    if job_type == "show_image" and argument not in ALLOWED_IMAGES:
        return jsonify(status="refused", reason="Unknown image; use smile, heart or checker"), 400
    with state_lock:
        expire_pending_jobs()
        job = {"id": next_job_id, "job": job_type, "arg": argument,
               "status": "waiting", "created_at": datetime.now()}
        next_job_id += 1
        jobs[job["id"]] = job
        pending_jobs.append(job["id"])
        last_job = job
        return jsonify(job_id=job["id"], status="accepted"), 201


@app.route("/api/poll", methods=["POST"])
def poll():
    global last_seen
    if request.headers.get("X-API-Key") != ATOM_API_KEY:
        return jsonify(error="unauthorized"), 401
    with state_lock:
        last_seen = datetime.now()
        expire_pending_jobs()
        if not pending_jobs:
            return jsonify(msg=None)
        job = jobs[pending_jobs.popleft()]
        job["status"] = "sent"
        return jsonify(msg=job["id"], job=job["job"], arg=job["arg"])


@app.route("/api/result", methods=["POST"])
def result():
    if request.headers.get("X-API-Key") != ATOM_API_KEY:
        return jsonify(error="unauthorized"), 401
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or type(data.get("id")) is not int:
        return jsonify(error="Invalid job ID"), 400
    job_id, value = data["id"], data.get("result")
    if value not in ("Atom Accepted", "done", "refused", "error"):
        return jsonify(error="Invalid result"), 400
    with state_lock:
        job = jobs.get(job_id)
        if job is None:
            return jsonify(error="Unknown job"), 400
        # A retry or late intermediate acknowledgement cannot undo completion.
        if job["status"] in FINAL_RESULTS:
            if value == job["status"] or value == "Atom Accepted":
                return jsonify(status="ok")
            return jsonify(error="Conflicting final result"), 409
        if job["status"] == "waiting":
            return jsonify(error="Job has not been dispatched"), 409
        job["status"] = value
        return jsonify(status="ok")


@app.route("/api/status")
def status():
    with state_lock:
        expire_pending_jobs()
        online = (last_seen is not None and
                  (datetime.now() - last_seen).total_seconds() <= ONLINE_TIMEOUT_SECONDS)
        return jsonify(
            robot_status="ONLINE" if online else "OFFLINE",
            last_seen=last_seen.astimezone().isoformat(timespec="seconds") if last_seen else None,
            last_job=public_job(last_job) if last_job else None,
            queue_length=len(pending_jobs),
            jobs=[public_job(job) for job in list(jobs.values())[-50:]],
        )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
