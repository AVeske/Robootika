import os
import unittest
from datetime import datetime, timedelta
os.environ["ATOM_API_KEY"] = "test-key"
import app as server

class ApiTests(unittest.TestCase):
    def setUp(self):
        server.current_job = server.last_job = server.last_seen = None
        server.next_job_id = 1
        self.client = server.app.test_client()
        self.headers = {"X-API-Key": "test-key"}

    def create(self, job="letter", arg="A"):
        return self.client.post("/api/jobs", json={"job": job, "arg": arg})

    def poll(self):
        return self.client.post("/api/poll", headers=self.headers)

    def test_both_jobs(self):
        for job, arg in (("letter", "K"), ("show_image", "smile")):
            created = self.create(job, arg)
            self.assertEqual(created.status_code, 201)
            job_id = created.json["job_id"]
            self.assertEqual(self.poll().json, {"msg": job_id, "job": job, "arg": arg})
            self.assertIsNone(self.poll().json["msg"])
            for _ in range(2):
                response = self.client.post("/api/result", headers=self.headers,
                    json={"id": job_id, "result": "done"})
                self.assertEqual(response.status_code, 200)

    def test_refused_and_busy(self):
        self.create()
        for job, arg in (("unknown", None), ("letter", "AB"), ("show_image", "invalid")):
            response = self.create(job, arg)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json["status"], "refused")
        self.assertEqual(self.create().status_code, 409)
        self.assertEqual(server.current_job["id"], 1)
        self.poll()
        self.assertEqual(self.create().status_code, 409)

    def test_expiry(self):
        for via_status in (True, False):
            self.create()
            server.current_job["created_at"] -= timedelta(seconds=31)
            if via_status:
                self.assertEqual(self.client.get("/api/status").json["last_job"]["status"], "expired")
            self.assertIsNone(self.poll().json["msg"])
            self.assertEqual(server.last_job["status"], "expired")
            response = self.client.post("/api/result", headers=self.headers,
                json={"id": server.last_job["id"], "result": "done"})
            self.assertEqual(response.status_code, 409)

    def test_presence(self):
        self.assertEqual(self.client.get("/api/status").json["robot_status"], "OFFLINE")
        self.assertEqual(self.client.post("/api/poll").status_code, 401)
        self.assertIsNone(server.last_seen)
        self.poll()
        status = self.client.get("/api/status").json
        self.assertEqual(status["robot_status"], "ONLINE")
        self.assertIsNotNone(datetime.fromisoformat(status["last_seen"]).tzinfo)
        server.last_seen -= timedelta(seconds=11)
        self.assertEqual(self.client.get("/api/status").json["robot_status"], "OFFLINE")

    def test_payload_and_page(self):
        for endpoint in ("jobs", "result"):
            self.assertEqual(self.client.post("/api/" + endpoint, headers=self.headers, json=[1]).status_code, 400)
        self.assertIn(b'value="show_image"', self.client.get("/").data)
