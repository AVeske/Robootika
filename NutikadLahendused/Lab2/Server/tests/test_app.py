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
