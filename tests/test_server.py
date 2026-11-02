"""Unit tests for Starlette Web Dashboard and REST API endpoints."""
import os
import unittest
import tempfile
from pathlib import Path
from starlette.testclient import TestClient

class TestServerAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.db_path = Path(cls.temp_dir.name) / "test_api.db"
        os.environ["APP_TRACKER_DB"] = str(cls.db_path)

        from tracker import db
        db.init_db(cls.db_path)

        from tracker.server import app
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()
        os.environ.pop("APP_TRACKER_DB", None)

    def test_get_dashboard_html(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Applications Tracker", resp.text)
        self.assertIn("text/html", resp.headers["content-type"])

    def test_post_and_get_applications(self):
        # 1. Post valid application
        payload = {
            "company": "KCB Bank",
            "role": "Cloud Infrastructure Architect",
            "location_type": "NAIROBI",
            "compensation": "KES 400,000",
            "channel": "Direct",
            "notes": "Core banking migration to Kubernetes"
        }
        res_post = self.client.post("/api/applications", json=payload)
        self.assertEqual(res_post.status_code, 201)
        data = res_post.json()
        self.assertIn("id", data)
        app_id = data["id"]

        # 2. Get list of applications
        res_list = self.client.get("/api/applications")
        self.assertEqual(res_list.status_code, 200)
        items = res_list.json()
        self.assertTrue(any(i["id"] == app_id for i in items))

        # 3. Get single application detail
        res_detail = self.client.get(f"/api/applications/{app_id}")
        self.assertEqual(res_detail.status_code, 200)
        detail = res_detail.json()
        self.assertEqual(detail["company"], "KCB Bank")
        self.assertEqual(len(detail["timeline"]), 1)

    def test_post_invalid_application_payload(self):
        res = self.client.post("/api/applications", json={"company": ""})
        self.assertEqual(res.status_code, 400)
        self.assertIn("error", res.json())

    def test_get_nonexistent_application(self):
        res = self.client.get("/api/applications/99999")
        self.assertEqual(res.status_code, 404)

    def test_patch_application_status(self):
        # Create an app first
        res_post = self.client.post("/api/applications", json={
            "company": "GitLab",
            "role": "SRE Systems Engineer",
            "location_type": "REMOTE_GLOBAL"
        })
        app_id = res_post.json()["id"]

        # Valid status patch
        res_patch = self.client.patch(f"/api/applications/{app_id}/status", json={
            "status": "TECHNICAL",
            "note": "Passed preliminary round"
        })
        self.assertEqual(res_patch.status_code, 200)
        self.assertEqual(res_patch.json()["new_status"], "TECHNICAL")

        # Invalid status patch
        res_bad = self.client.patch(f"/api/applications/{app_id}/status", json={
            "status": "NON_EXISTENT_STATUS"
        })
        self.assertEqual(res_bad.status_code, 400)

        # Non-existent app patch
        res_404 = self.client.patch("/api/applications/99999/status", json={"status": "OFFER"})
        self.assertEqual(res_404.status_code, 404)

    def test_delete_application(self):
        res_post = self.client.post("/api/applications", json={
            "company": "DiscardCo",
            "role": "QA Engineer"
        })
        app_id = res_post.json()["id"]

        res_del = self.client.delete(f"/api/applications/{app_id}")
        self.assertEqual(res_del.status_code, 200)

        # Deleting again returns 404
        res_del_again = self.client.delete(f"/api/applications/{app_id}")
        self.assertEqual(res_del_again.status_code, 404)

    def test_get_metrics_telemetry(self):
        res = self.client.get("/api/metrics")
        self.assertEqual(res.status_code, 200)
        metrics = res.json()
        self.assertIn("total_applications", metrics)
        self.assertIn("interview_rate_pct", metrics)
        self.assertIn("funnel", metrics)

if __name__ == "__main__":
    unittest.main()
