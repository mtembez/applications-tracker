"""End-to-End System Lifecycle Integration Test."""
import os
import unittest
import tempfile
from pathlib import Path
from starlette.testclient import TestClient

from tracker import db, cli
from tracker.models import AppStatus, LocationType
from tracker.server import app

class TestSystemEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.db_path = Path(cls.temp_dir.name) / "test_e2e.db"
        os.environ["APP_TRACKER_DB"] = str(cls.db_path)
        db.init_db(cls.db_path)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()
        os.environ.pop("APP_TRACKER_DB", None)

    def test_full_application_lifecycle(self):
        # Step 1: Add application via CLI layer
        add_args = cli.argparse.Namespace(
            company="Cloudflare",
            role="Edge Systems & Rust Engineer",
            location="REMOTE_GLOBAL",
            status="APPLIED",
            compensation="$6,500/mo",
            channel="Direct Engineering Referral",
            url="https://www.cloudflare.com/careers",
            notes="Requires socket programming and low-level Linux networking"
        )
        cli.cmd_add(add_args)

        # Step 2: Query application via Starlette Web API
        res_list = self.client.get("/api/applications")
        self.assertEqual(res_list.status_code, 200)
        apps = res_list.json()
        self.assertEqual(len(apps), 1)
        app_id = apps[0]["id"]
        self.assertEqual(apps[0]["company"], "Cloudflare")
        self.assertEqual(apps[0]["status"], "APPLIED")

        # Step 3: Transition to SCREENING via Web API
        res_patch1 = self.client.patch(f"/api/applications/{app_id}/status", json={
            "status": "SCREENING",
            "note": "HR screen scheduled for Tuesday"
        })
        self.assertEqual(res_patch1.status_code, 200)

        # Step 4: Advance to TECHNICAL via CLI command
        status_args = cli.argparse.Namespace(
            id=app_id,
            new_status="TECHNICAL",
            note="Systems architecture and live socket programming challenge"
        )
        cli.cmd_status(status_args)

        # Step 5: Advance to OFFER via Web API
        res_patch2 = self.client.patch(f"/api/applications/{app_id}/status", json={
            "status": "OFFER",
            "note": "Offer package received: $6,500/mo + equity"
        })
        self.assertEqual(res_patch2.status_code, 200)

        # Step 6: Verify Telemetry Metrics via Web API
        res_metrics = self.client.get("/api/metrics")
        self.assertEqual(res_metrics.status_code, 200)
        metrics = res_metrics.json()
        self.assertEqual(metrics["total_applications"], 1)
        self.assertEqual(metrics["active_applications"], 1)
        self.assertEqual(metrics["interview_count"], 1)
        self.assertEqual(metrics["offer_count"], 1)
        self.assertEqual(metrics["offer_rate_pct"], 100.0)

        # Step 7: Inspect application history and timeline
        detail = db.get_application(app_id, self.db_path)
        self.assertEqual(detail["status"], "OFFER")
        # 1 CREATED + 3 STATUS_CHANGE events
        self.assertEqual(len(detail["timeline"]), 4)
        self.assertEqual(detail["timeline"][0]["event_type"], "CREATED")
        self.assertIn("SCREENING", detail["timeline"][1]["details"])
        self.assertIn("TECHNICAL", detail["timeline"][2]["details"])
        self.assertIn("OFFER", detail["timeline"][3]["details"])

        # Step 8: Delete application via Web API
        res_del = self.client.delete(f"/api/applications/{app_id}")
        self.assertEqual(res_del.status_code, 200)

        # Step 9: Verify complete cascade purge in DB
        self.assertIsNone(db.get_application(app_id, self.db_path))
        conn = db.get_connection(self.db_path)
        ev_count = conn.execute("SELECT COUNT(*) FROM timeline_events WHERE app_id = ?", (app_id,)).fetchone()[0]
        self.assertEqual(ev_count, 0)
        conn.close()

if __name__ == "__main__":
    unittest.main()
