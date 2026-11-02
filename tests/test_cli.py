"""Unit tests for the Rich Command-Line Interface."""
import os
import io
import sys
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from tracker import db
from tracker import cli
from tracker.models import ApplicationCreate, AppStatus, LocationType

class TestCLICommands(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_cli.db"
        os.environ["APP_TRACKER_DB"] = str(self.db_path)
        db.init_db(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()
        os.environ.pop("APP_TRACKER_DB", None)

    def test_cli_add_and_list(self):
        # Test adding via mock args
        args = cli.argparse.Namespace(
            company="Red Hat",
            role="Kernel Engineer",
            location="REMOTE_EMEA",
            status="APPLIED",
            compensation="$6,000/mo",
            channel="Direct",
            url="https://redhat.com/jobs",
            notes="Requires C and Linux internals"
        )
        cli.cmd_add(args)

        apps = db.list_applications(db_path=self.db_path)
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0]["company"], "Red Hat")

        # Test listing
        list_args = cli.argparse.Namespace(status=None, search=None)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            cli.cmd_list(list_args)
            # Table prints without crash
            self.assertIsNotNone(mock_stdout.getvalue())

    def test_cli_view_and_missing_id(self):
        app_id = db.create_application(
            ApplicationCreate(company="Canonical", role="Cloud Init Engineer"),
            self.db_path
        )
        view_args = cli.argparse.Namespace(id=app_id)
        with patch("sys.stdout", new_callable=io.StringIO):
            cli.cmd_view(view_args)

        # Invalid ID should exit with code 1
        bad_args = cli.argparse.Namespace(id=99999)
        with self.assertRaises(SystemExit) as cm:
            cli.cmd_view(bad_args)
        self.assertEqual(cm.exception.code, 1)

    def test_cli_status_transition(self):
        app_id = db.create_application(
            ApplicationCreate(company="HashiCorp", role="Go/Terraform Engineer"),
            self.db_path
        )
        stat_args = cli.argparse.Namespace(
            id=app_id,
            new_status="TECHNICAL",
            note="Completed code challenge"
        )
        cli.cmd_status(stat_args)

        record = db.get_application(app_id, self.db_path)
        self.assertEqual(record["status"], "TECHNICAL")

        # Invalid status should exit with code 1
        bad_stat_args = cli.argparse.Namespace(
            id=app_id,
            new_status="NOT_A_STATUS",
            note=None
        )
        with self.assertRaises(SystemExit) as cm:
            cli.cmd_status(bad_stat_args)
        self.assertEqual(cm.exception.code, 1)

    def test_cli_metrics(self):
        metrics_args = cli.argparse.Namespace()
        with patch("sys.stdout", new_callable=io.StringIO):
            cli.cmd_metrics(metrics_args)

    def test_cli_export_json_and_csv(self):
        db.create_application(
            ApplicationCreate(company="Docker", role="Core Engine Engineer"),
            self.db_path
        )

        # JSON export
        json_args = cli.argparse.Namespace(format="json")
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            cli.cmd_export(json_args)
            out = mock_stdout.getvalue()
            self.assertIn("Docker", out)
            self.assertIn("Core Engine Engineer", out)

        # CSV export
        csv_args = cli.argparse.Namespace(format="csv")
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            cli.cmd_export(csv_args)
            out = mock_stdout.getvalue()
            self.assertIn("company,role", out)
            self.assertIn("Docker", out)

if __name__ == "__main__":
    unittest.main()
