"""Unit tests for SQLite WAL persistence layer, integrity, and queries."""
import unittest
import tempfile
import sqlite3
from pathlib import Path

from tracker import db
from tracker.models import ApplicationCreate, AppStatus, LocationType, EventType

class TestDatabaseLayer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_layer.db"
        db.init_db(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_wal_mode_and_pragmas(self):
        conn = db.get_connection(self.db_path)
        cursor = conn.cursor()
        
        journal_mode = cursor.execute("PRAGMA journal_mode;").fetchone()[0]
        self.assertEqual(journal_mode.lower(), "wal")
        
        foreign_keys = cursor.execute("PRAGMA foreign_keys;").fetchone()[0]
        self.assertEqual(foreign_keys, 1)
        
        conn.close()

    def test_foreign_key_violation(self):
        conn = db.get_connection(self.db_path)
        with self.assertRaises(sqlite3.IntegrityError):
            with conn:
                conn.execute(
                    "INSERT INTO timeline_events (app_id, event_type, details, created_at) VALUES (?, ?, ?, ?)",
                    (99999, "INVALID", "Non-existent parent", "2026-01-01T00:00:00Z")
                )
        conn.close()

    def test_create_minimal_application(self):
        app = ApplicationCreate(company="Canonical", role="Ubuntu Systems Engineer")
        app_id = db.create_application(app, self.db_path)
        self.assertGreater(app_id, 0)

        record = db.get_application(app_id, self.db_path)
        self.assertEqual(record["company"], "Canonical")
        self.assertEqual(record["role"], "Ubuntu Systems Engineer")
        self.assertEqual(record["status"], AppStatus.APPLIED.value)
        self.assertEqual(len(record["timeline"]), 1)
        self.assertEqual(record["timeline"][0]["event_type"], EventType.CREATED.value)

    def test_update_status_and_timeline_audit(self):
        app = ApplicationCreate(company="Amazon AWS", role="Cloud Support Engineer")
        app_id = db.create_application(app, self.db_path)

        res = db.update_status(app_id, AppStatus.TECHNICAL, note="Passed phone screen", db_path=self.db_path)
        self.assertTrue(res)

        record = db.get_application(app_id, self.db_path)
        self.assertEqual(record["status"], AppStatus.TECHNICAL.value)
        self.assertEqual(len(record["timeline"]), 2)
        self.assertEqual(record["timeline"][1]["event_type"], EventType.STATUS_CHANGE.value)
        self.assertIn("Passed phone screen", record["timeline"][1]["details"])

    def test_update_nonexistent_application(self):
        res = db.update_status(8888, AppStatus.OFFER, db_path=self.db_path)
        self.assertFalse(res)

    def test_add_custom_event(self):
        app_id = db.create_application(ApplicationCreate(company="Turing", role="Python Dev"), self.db_path)
        ok = db.add_event(app_id, EventType.INTERVIEW_SCHEDULED, "Round 1 set for Thursday 14:00 EAT", self.db_path)
        self.assertTrue(ok)

        record = db.get_application(app_id, self.db_path)
        self.assertEqual(len(record["timeline"]), 2)
        self.assertEqual(record["timeline"][1]["event_type"], EventType.INTERVIEW_SCHEDULED.value)

        # Invalid app_id
        bad_ok = db.add_event(99999, EventType.NOTE_ADDED, "Note", self.db_path)
        self.assertFalse(bad_ok)

    def test_list_applications_filtering_and_search(self):
        db.create_application(ApplicationCreate(company="Stripe", role="API Infra", status=AppStatus.TECHNICAL), self.db_path)
        db.create_application(ApplicationCreate(company="GitLab", role="SRE Backend", status=AppStatus.APPLIED), self.db_path)
        db.create_application(ApplicationCreate(company="LocalTech", role="Frontend", status=AppStatus.REJECTED), self.db_path)

        # Filter by status
        tech_apps = db.list_applications(status="TECHNICAL", db_path=self.db_path)
        self.assertEqual(len(tech_apps), 1)
        self.assertEqual(tech_apps[0]["company"], "Stripe")

        # Search by company
        search_git = db.list_applications(search="gitlab", db_path=self.db_path)
        self.assertEqual(len(search_git), 1)
        self.assertEqual(search_git[0]["company"], "GitLab")

        # Search by role
        search_infra = db.list_applications(search="infra", db_path=self.db_path)
        self.assertEqual(len(search_infra), 1)
        self.assertEqual(search_infra[0]["company"], "Stripe")

    def test_empty_metrics_no_division_by_zero(self):
        m = db.get_metrics(self.db_path)
        self.assertEqual(m["total_applications"], 0)
        self.assertEqual(m["active_applications"], 0)
        self.assertEqual(m["interview_rate_pct"], 0.0)
        self.assertEqual(m["offer_rate_pct"], 0.0)

    def test_delete_application_cascades(self):
        app_id = db.create_application(ApplicationCreate(company="Expensify", role="C++ Engineer"), self.db_path)
        db.update_status(app_id, AppStatus.TECHNICAL, db_path=self.db_path)

        conn = db.get_connection(self.db_path)
        ev_count = conn.execute("SELECT COUNT(*) FROM timeline_events WHERE app_id = ?", (app_id,)).fetchone()[0]
        self.assertEqual(ev_count, 2)
        conn.close()

        deleted = db.delete_application(app_id, self.db_path)
        self.assertTrue(deleted)

        conn = db.get_connection(self.db_path)
        ev_count_after = conn.execute("SELECT COUNT(*) FROM timeline_events WHERE app_id = ?", (app_id,)).fetchone()[0]
        self.assertEqual(ev_count_after, 0)
        conn.close()

        # Delete again returns False
        self.assertFalse(db.delete_application(app_id, self.db_path))

if __name__ == "__main__":
    unittest.main()
