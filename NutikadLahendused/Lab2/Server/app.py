import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# --------------------------------------------------
# Seaded
# --------------------------------------------------

# Atomi API võti.
# Loetakse environment variable'ist.
# Kui seda pole määratud, kasutatakse testimiseks CHANGE_ME.
ATOM_API_KEY = os.getenv("ATOM_API_KEY")

if not ATOM_API_KEY:
    raise RuntimeError("ATOM_API_KEY is not configured")

# Kui kaua töö serveris kehtib.
JOB_TTL_SECONDS = 30

# Kui Atom pole 10 sekundit serveriga rääkinud,
# loeme ta OFFLINE-iks.
ONLINE_TIMEOUT_SECONDS = 10

# Ainult need tööd on lubatud.
ALLOWED_JOBS = [
    "letter",
    "show_image",
]


# --------------------------------------------------
# Serveri ajutine mälu
# --------------------------------------------------

# Hetkel ootel olev töö.
current_job = None

# Viimane töö, mida kasutajale näitame.
last_job = None

# Millal Atom viimati /api/poll endpointi kutsus.
last_seen = None

# Järgmise töö ID.
next_job_id = 1

# Pildid peavad olema samade nimedega ka Atomi püsivaras.
ALLOWED_IMAGES = ("smile", "heart", "checker")


def expire_pending_job():
    global current_job
    if current_job is not None:
        age = (datetime.now() - current_job["created_at"]).total_seconds()
        if age >= JOB_TTL_SECONDS:
            current_job["status"] = "expired"
            current_job = None



# --------------------------------------------------
# Kasutaja veebileht
# --------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# --------------------------------------------------
# Uue töö lisamine
# POST /api/jobs
# --------------------------------------------------

@app.route("/api/jobs", methods=["POST"])
def create_job():
    global current_job, last_job, next_job_id

    data = request.get_json(silent=True) or {}

    if not isinstance(data, dict):
        return jsonify(status="refused", reason="JSON object required"), 400

    job_type = data.get("job")
    argument = data.get("arg")

    # Kontrollime, kas töö on lubatud.
    if job_type not in ALLOWED_JOBS:
        return jsonify({
            "status": "refused",
            "reason": "Unknown or forbidden job"
        }), 400

    # Kui töö on "letter", peab argument olema täpselt üks täht.
    if job_type == "letter":
        if not isinstance(argument, str) or len(argument) != 1:
            return jsonify({
                "status": "refused",
                "reason": "Letter must be exactly one character"
            }), 400

    # Loome uue töö.
    if job_type == "show_image" and argument not in ALLOWED_IMAGES:
        return jsonify(status="refused", reason="Unknown image; use smile, heart or checker"), 400
    expire_pending_job()
    if last_job is not None and last_job["status"] in ("waiting", "sent"):
        return jsonify(status="refused", reason="Another job is still active"), 409

    job = {
        "id": next_job_id,
        "job": job_type,
        "arg": argument,
        "status": "waiting",

        # datetime objekt jääb serverisse.
        # Seda kasutame hiljem töö vanuse arvutamiseks.
        "created_at": datetime.now()
    }

    next_job_id += 1

    current_job = job
    last_job = job

    return jsonify({
        "job_id": job["id"],
        "status": "accepted"
    }), 201


# --------------------------------------------------
# Atom küsib uut tööd
# POST /api/poll
# --------------------------------------------------

@app.route("/api/poll", methods=["POST"])
def poll():
    global current_job, last_job, last_seen

    # Kontrollime Atomi API key'd.
    api_key = request.headers.get("X-API-Key")

    if api_key != ATOM_API_KEY:
        return jsonify({
            "error": "unauthorized"
        }), 401

    # Atom võttis serveriga ühendust.
    last_seen = datetime.now()
    expire_pending_job()

    # Kui tööd pole, pole midagi anda.
    if current_job is None:
        return jsonify({
            "msg": None
        })

    # --------------------------------------------------
    # Kontrollime töö vanust
    # --------------------------------------------------

    age = (
        datetime.now()
        - current_job["created_at"]
    ).total_seconds()

    # Kui töö on vanem kui 30 sekundit,
    # ei tohi seda robotile anda.
    if age > JOB_TTL_SECONDS:

        current_job["status"] = "expired"

        last_job = current_job
        current_job = None

        return jsonify({
            "msg": None
        })

    # --------------------------------------------------
    # Töö on värske -> anname Atomile
    # --------------------------------------------------

    job = current_job

    # Eemaldame töö ootejärjekorrast.
    current_job = None

    job["status"] = "sent"
    last_job = job

    return jsonify({
        "msg": job["id"],
        "job": job["job"],
        "arg": job["arg"]
    })


# --------------------------------------------------
# Atom saadab töö tulemuse
# POST /api/result
# --------------------------------------------------

@app.route("/api/result", methods=["POST"])
def result():
    global last_job

    # Kontrollime Atomi API key'd.
    api_key = request.headers.get("X-API-Key")

    if api_key != ATOM_API_KEY:
        return jsonify({
            "error": "unauthorized"
        }), 401

    data = request.get_json(silent=True) or {}

    if not isinstance(data, dict):
        return jsonify(error="JSON object required"), 400

    job_id = data.get("id")
    result_value = data.get("result")

    # Kui server ei tea ühtegi tööd.
    if last_job is None:
        return jsonify({
            "error": "No job exists"
        }), 400

    # Kontrollime, kas tulemus kuulub õigele tööle.
    if job_id != last_job["id"]:
        return jsonify({
            "error": "Unknown job"
        }), 400

    # Lubatud tulemused.
    allowed_results = [
        "done",
        "refused",
        "error"
    ]

    if result_value not in allowed_results:
        return jsonify({
            "error": "Invalid result"
        }), 400

    if last_job["status"] != "sent":
        if last_job["status"] == result_value:
            return jsonify(status="ok")
        return jsonify(error="Job is not awaiting a result"), 409

    # Salvestame tulemuse.
    if last_job["status"] != "sent":
        if last_job["status"] == result_value:
            return jsonify(status="ok")
        return jsonify(error="Job is not awaiting a result"), 409

    last_job["status"] = result_value

    return jsonify({
        "status": "ok"
    })


# --------------------------------------------------
# Veebileht küsib staatust
# GET /api/status
# --------------------------------------------------

@app.route("/api/status")
def status():
    expire_pending_job()

    # --------------------------------------------------
    # ONLINE / OFFLINE
    # --------------------------------------------------

    if last_seen is None:

        robot_status = "OFFLINE"

    else:

        seconds_since_seen = (
            datetime.now()
            - last_seen
        ).total_seconds()

        if seconds_since_seen <= ONLINE_TIMEOUT_SECONDS:
            robot_status = "ONLINE"
        else:
            robot_status = "OFFLINE"

    # --------------------------------------------------
    # Valmistame last_job brauserile saatmiseks
    # --------------------------------------------------

    job_for_response = None

    if last_job is not None:

        job_for_response = {
            "id": last_job["id"],
            "job": last_job["job"],
            "arg": last_job["arg"],
            "status": last_job["status"]
        }

    return jsonify({
        "robot_status": robot_status,

        "last_seen": (
            last_seen.astimezone().isoformat(timespec="seconds")
            if last_seen
            else None
        ),

        "last_job": job_for_response
    })


# --------------------------------------------------
# Flask server
# --------------------------------------------------

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)