import io
import os
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path
from PIL import Image
os.environ["ATOM_API_KEY"] = "test-key"
import app as server


class ApiTests(unittest.TestCase):
    def setUp(self):
        server.jobs.clear()
        server.pending_jobs.clear()
        server.last_job = server.last_seen = None
        server.next_job_id = 1
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.old_directory = server.app.config["IMAGE_DIR"]
        server.app.config["IMAGE_DIR"] = self.directory.name
        self.addCleanup(server.app.config.update, IMAGE_DIR=self.old_directory)
        self.client = server.app.test_client()
        self.headers = {"X-API-Key": "test-key"}

    def upload(self, raw=None):
        if raw is None:
            buffer = io.BytesIO()
            Image.new("RGBA", (300, 100), (255, 0, 0, 128)).save(buffer, "PNG")
            raw = buffer.getvalue()
        return self.client.post("/api/images", data={"file": (io.BytesIO(raw), "picture.png")})

    def create(self, job="letter", arg="A"):
        return self.client.post("/api/jobs", json={"job": job, "arg": arg})

    def poll(self):
        return self.client.post("/api/poll", headers=self.headers)

    def test_image_upload_list_job_download_and_result(self):
        uploaded = self.upload()
        self.assertEqual(uploaded.status_code, 201)
        image_id = uploaded.json["id"]
        self.assertEqual(self.client.get("/api/images").json["images"][0]["id"], image_id)
        self.assertEqual(self.upload().json["id"], image_id)
        self.assertEqual(len(list(Path(self.directory.name).glob("*.png"))), 1)
        created = self.create("show_image", image_id)
        self.assertEqual(created.status_code, 201)
        payload = self.poll().json
        self.assertEqual(payload["arg"], image_id)
        self.assertEqual(self.client.get(payload["image_url"]).status_code, 401)
        downloaded = self.client.get(payload["image_url"], headers=self.headers)
        self.assertEqual(downloaded.mimetype, "image/png")
        raw = downloaded.data
        downloaded.close()
        preview = self.client.get("/api/images/" + image_id + "/preview")
        self.assertEqual(preview.status_code, 200)
        self.assertEqual(preview.mimetype, "image/png")
        self.assertEqual(preview.data, raw)
        preview.close()
        with Image.open(io.BytesIO(raw)) as image:
            self.assertEqual(image.size, (128, 128))
            self.assertEqual(image.mode, "RGB")
        for value in ("Atom Accepted", "done", "done", "Atom Accepted"):
            response = self.client.post("/api/result", headers=self.headers,
                json={"id": created.json["job_id"], "result": value})
            self.assertEqual(response.status_code, 200)
        self.assertEqual(server.last_job["status"], "done")

    def test_invalid_uploads_and_ids(self):
        self.assertEqual(self.upload(b"not png").status_code, 400)
        buffer = io.BytesIO()
        Image.new("RGB", (10, 10)).save(buffer, "JPEG")
        self.assertEqual(self.upload(buffer.getvalue()).status_code, 400)
        self.assertEqual(self.upload(b"x" * (1024 * 1024 + 1)).status_code, 413)
        buffer = io.BytesIO()
        Image.new("RGB", (2049, 1)).save(buffer, "PNG")
        self.assertEqual(self.upload(buffer.getvalue()).status_code, 400)
        self.assertEqual(self.client.post("/api/images").status_code, 400)
        for arg in ("smile", "../secret", None, [], "f" * 64):
            self.assertEqual(self.create("show_image", arg).status_code, 400)
        self.assertEqual(self.client.get("/api/images/invalid/png", headers=self.headers).status_code, 404)

    def test_unknown_preview(self):
        for image_id in ("invalid", "f" * 64):
            self.assertEqual(self.client.get("/api/images/" + image_id + "/preview").status_code, 404)

    def test_fifo_and_refusal(self):
        self.assertEqual(self.create().status_code, 201)
        self.assertEqual(self.create("letter", "b").status_code, 201)
        for job, arg in (("unknown", None), ("letter", "AB")):
            response = self.create(job, arg)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json["status"], "refused")
        self.assertEqual(self.poll().json["arg"], "A")
        self.assertEqual(self.poll().json["arg"], "B")
        self.assertIsNone(self.poll().json["msg"])

    def test_expiry_and_presence(self):
        self.create()
        server.last_job["created_at"] -= timedelta(seconds=31)
        status = self.client.get("/api/status").json
        self.assertEqual(status["last_job"]["status"], "expired")
        self.assertEqual(status["robot_status"], "OFFLINE")
        self.assertEqual(self.client.post("/api/poll").status_code, 401)
        self.assertIsNone(server.last_seen)
        self.assertIsNone(self.poll().json["msg"])
        self.assertEqual(self.client.get("/api/status").json["robot_status"], "ONLINE")
        server.last_seen -= timedelta(seconds=11)
        status = self.client.get("/api/status").json
        self.assertEqual(status["robot_status"], "OFFLINE")
        self.assertIsNotNone(status["last_seen"])

    def test_page(self):
        page = self.client.get("/").data
        self.assertIn(b'type="file"', page)
        self.assertIn(b'/api/images', page)

    def test_rejected_jobs_never_reach_atom(self):
        for job, arg in (("unknown", "A"), ("move", "10"), ("letter", "1"),
                         ("letter", "AB"), ("letter", ""), ("letter", 7),
                         ("letter", "ß"), ("letter", None)):
            with self.subTest(job=job, arg=arg):
                response = self.create(job, arg)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json["status"], "refused")
                self.assertIsNone(self.poll().json["msg"])
        self.assertEqual(len(server.jobs), 0)

    def test_only_ascii_letters_are_accepted(self):
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            with self.subTest(letter=letter):
                self.assertEqual(self.create(arg=letter).status_code, 201)
                self.assertEqual(self.poll().json["arg"], letter.upper())
        self.assertIsNone(self.poll().json["msg"])

    def test_invalid_input_preserves_pending_work(self):
        accepted_id = self.create(arg="B").json["job_id"]
        invalid = list("0123456789") + [0, 7, 1.5, True, None, [], {},
            "", "AB", "A1", " A", "A ", "A\n", "!", "õ", "Ä", "ß", "ı", "ſ", "１", "😀"]
        payloads = [{"job": "letter", "arg": arg} for arg in invalid]
        payloads += [{"job": job, "arg": "A"} for job in
                     ("unknown", "move", "LETTER", "", None, 7, [], {})]
        payloads += [None, [], "A", 7, {}, {"job": "letter"}]
        for payload in payloads:
            with self.subTest(payload=payload):
                response = self.client.post("/api/jobs", json=payload)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json["status"], "refused")
                self.assertEqual(list(server.pending_jobs), [accepted_id])
                self.assertEqual(list(server.jobs), [accepted_id])
                self.assertEqual(server.next_job_id, 2)
        self.assertEqual(self.poll().json["msg"], accepted_id)
        self.assertIsNone(self.poll().json["msg"])

    def test_poll_expires_old_job_without_status_request(self):
        old_id = self.create().json["job_id"]
        fresh_id = self.create("letter", "B").json["job_id"]
        server.jobs[old_id]["created_at"] -= timedelta(seconds=31)
        self.assertEqual(self.poll().json["msg"], fresh_id)
        self.assertEqual(server.jobs[old_id]["status"], "expired")
        self.assertIsNone(self.poll().json["msg"])
        response = self.client.post("/api/result", headers=self.headers,
            json={"id": old_id, "result": "done"})
        self.assertEqual(response.status_code, 409)

    def test_dispatched_job_can_finish_after_long_outage(self):
        job_id = self.create().json["job_id"]
        self.assertEqual(self.poll().json["msg"], job_id)
        server.jobs[job_id]["created_at"] -= timedelta(seconds=120)
        server.last_seen -= timedelta(seconds=120)
        status = self.client.get("/api/status").json
        self.assertEqual(status["robot_status"], "OFFLINE")
        self.assertEqual(status["last_job"]["status"], "sent")
        # Simulate delivery after connectivity returns, including an HTTP retry.
        for _ in range(2):
            response = self.client.post("/api/result", headers=self.headers,
                json={"id": job_id, "result": "done"})
            self.assertEqual(response.status_code, 200)
        self.assertEqual(server.jobs[job_id]["status"], "done")
        self.assertIsNone(self.poll().json["msg"])

    def test_unauthorized_poll_does_not_consume_job(self):
        job_id = self.create().json["job_id"]
        self.assertEqual(self.client.post("/api/poll").status_code, 401)
        self.assertIsNone(server.last_seen)
        self.assertEqual(self.poll().json["msg"], job_id)
