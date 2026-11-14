import os
import hashlib
import io
import re
import warnings
from pathlib import Path
import threading
from collections import deque
from datetime import datetime

from flask import Flask, jsonify, render_template, request, send_file, url_for
from PIL import Image, UnidentifiedImageError
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
ATOM_API_KEY = os.getenv("ATOM_API_KEY")
if not ATOM_API_KEY:
    raise RuntimeError("ATOM_API_KEY is not configured")

JOB_TTL_SECONDS = 30
ONLINE_TIMEOUT_SECONDS = 10
ALLOWED_JOBS = ["letter", "show_image"]
# PNGs persist across restarts; jobs remain in RAM.
app.config["IMAGE_DIR"] = os.getenv("IMAGE_DIR", str(Path(app.instance_path) / "images"))
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 + 65536
MAX_UPLOAD_BYTES = 1024 * 1024


def image_path(image_id):
    if not isinstance(image_id, str) or not re.fullmatch(r"[0-9a-f]{64}", image_id):
        return None
    return Path(app.config["IMAGE_DIR"]) / (image_id + ".png")


@app.errorhandler(413)
def upload_too_large(error):
    return jsonify(status="refused", reason="PNG upload limit is 1 MiB"), 413


@app.route("/api/images", methods=["GET", "POST"])
def images():
    directory = Path(app.config["IMAGE_DIR"])
    if request.method == "GET":
        files = sorted(directory.glob("*.png")) if directory.exists() else []
        return jsonify(images=[{"id": p.stem, "name": p.stem[:12] + ".png"}
                               for p in files if image_path(p.stem) is not None])
    upload = request.files.get("file")
    if upload is None:
        return jsonify(status="refused", reason="PNG file required in field file"), 400
    raw = upload.read(MAX_UPLOAD_BYTES + 1)
    if len(raw) > MAX_UPLOAD_BYTES:
        return upload_too_large(None)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(raw)) as source:
                if source.format != "PNG" or getattr(source, "n_frames", 1) != 1:
                    raise ValueError("Only static PNG images are supported")
                if not (1 <= source.width <= 2048 and 1 <= source.height <= 2048):
                    raise ValueError("Image dimensions must not exceed 2048 x 2048")
                source.load()
                # Fit the AtomS3R screen, flatten transparency onto black.
                source.thumbnail((128, 128))
                rgba = source.convert("RGBA")
                canvas = Image.new("RGB", (128, 128), "black")
                canvas.paste(rgba, ((128-rgba.width)//2, (128-rgba.height)//2), rgba)
                output = io.BytesIO()
                canvas.save(output, format="PNG")
                normalized = output.getvalue()
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError,
            Image.DecompressionBombError, Image.DecompressionBombWarning):
        return jsonify(status="refused", reason="Invalid PNG; use a static PNG up to 2048 x 2048"), 400
    image_id = hashlib.sha256(normalized).hexdigest()
    directory.mkdir(parents=True, exist_ok=True)
    image_path(image_id).write_bytes(normalized)
    return jsonify(id=image_id, name=image_id[:12] + ".png", width=128, height=128), 201


@app.route("/api/images/<image_id>/preview")
def preview_image(image_id):
    # Browser access follows the control page's access policy (e.g. Caddy auth).
    # The Atom key stays out of browser JavaScript and image URLs.
    path = image_path(image_id)
    if path is None or not path.is_file():
        return jsonify(error="Unknown image"), 404
    return send_file(path, mimetype="image/png", conditional=True)


@app.route("/api/images/<image_id>/png")
def download_image(image_id):
    if request.headers.get("X-API-Key") != ATOM_API_KEY:
        return jsonify(error="unauthorized"), 401
    path = image_path(image_id)
    if path is None or not path.is_file():
        return jsonify(error="Unknown image"), 404
    return send_file(path, mimetype="image/png", conditional=True)

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
        # Check the original input: Unicode uppercasing can turn non-ASCII
        # characters such as dotless i into an otherwise allowed letter.
        if not isinstance(argument, str) or re.fullmatch(r"[A-Za-z]", argument) is None:
            return jsonify(status="refused", reason="Letter must be A-Z"), 400
        argument = argument.upper()
    if job_type == "show_image":
        path = image_path(argument)
        if path is None or not path.is_file():
            return jsonify(status="refused", reason="Select an uploaded image"), 400
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
        payload = dict(msg=job["id"], job=job["job"], arg=job["arg"])
        if job["job"] == "show_image":
            payload["image_url"] = url_for("download_image", image_id=job["arg"])
        return jsonify(payload)


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
