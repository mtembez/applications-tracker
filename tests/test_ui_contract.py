"""UI Contract and Markup Structure tests for Multicolor Animated Console with Celestial Lion."""
import os
import unittest
import tempfile
from pathlib import Path
from starlette.testclient import TestClient

from tracker import db
from tracker.server import app

class TestUIContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.db_path = Path(cls.temp_dir.name) / "test_ui.db"
        os.environ["APP_TRACKER_DB"] = str(cls.db_path)
        db.init_db(cls.db_path)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()
        os.environ.pop("APP_TRACKER_DB", None)

    def test_html5_structure_and_doctype(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        html = resp.text
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn('<html lang="en" class="dark">', html)
        self.assertIn("<head>", html)
        self.assertIn("<body>", html)

    def test_multicolor_tokens_and_typography(self):
        resp = self.client.get("/")
        html = resp.text
        # Typography verification (Geist)
        self.assertIn("fonts.googleapis.com/css2?family=Geist", html)
        # Vibrant Multicolor Palette Tokens
        self.assertIn("--cyan: #06b6d4;", html)
        self.assertIn("--sky: #38bdf8;", html)
        self.assertIn("--violet: #8b5cf6;", html)
        self.assertIn("--emerald: #10b981;", html)
        self.assertIn("--amber: #f59e0b;", html)
        self.assertIn("--rose: #f43f5e;", html)

    def test_celestial_lion_background_artwork(self):
        resp = self.client.get("/")
        html = resp.text
        # Assert Celestial Lion SVG and geometric constellation markup
        self.assertIn('id="celestialLion"', html)
        self.assertIn('class="lion-backdrop-canvas"', html)
        self.assertIn('id="lionAurora"', html)
        self.assertIn('id="lionMane"', html)
        self.assertIn("<polygon", html)

    def test_magic_ui_aurora_and_shimmer_animations(self):
        resp = self.client.get("/")
        html = resp.text
        # Magic UI ambient gradient spheres
        self.assertIn('class="aurora-bg"', html)
        self.assertIn('class="aurora-sphere sphere-1"', html)
        self.assertIn('class="aurora-sphere sphere-2"', html)
        self.assertIn('class="shimmer-text"', html)

    def test_sidebar_and_navigation_structure(self):
        resp = self.client.get("/")
        html = resp.text
        self.assertIn("<aside>", html)
        self.assertIn('class="workspace-header"', html)
        self.assertIn('class="cmd-trigger"', html)
        self.assertIn('id="navAll"', html)
        self.assertIn('id="navActive"', html)
        self.assertIn('id="navInterviews"', html)
        self.assertIn('id="navOffers"', html)

    def test_linear_metrics_stats_strip(self):
        resp = self.client.get("/")
        html = resp.text
        self.assertIn('class="stats-strip"', html)
        self.assertIn('id="mTotal"', html)
        self.assertIn('id="mActive"', html)
        self.assertIn('id="mInterviews"', html)
        self.assertIn('id="mOffers"', html)

    def test_dual_view_containers(self):
        resp = self.client.get("/")
        html = resp.text
        self.assertIn('id="kanbanBoard"', html)
        self.assertIn('id="btnKanban"', html)
        self.assertIn('id="tableView"', html)
        self.assertIn('id="btnTable"', html)
        self.assertIn('class="data-table"', html)

    def test_slide_over_drawer_contract(self):
        resp = self.client.get("/")
        html = resp.text
        self.assertIn('id="slideDrawer"', html)
        self.assertIn('id="drawerOverlay"', html)
        self.assertIn('id="dMonogram"', html)
        self.assertIn('id="dStatusSelect"', html)
        self.assertIn('id="dTimeline"', html)

    def test_command_palette_cmdk_contract(self):
        resp = self.client.get("/")
        html = resp.text
        self.assertIn('id="cmdkModal"', html)
        self.assertIn('id="cmdkSearch"', html)
        self.assertIn('id="cmdkResults"', html)
        self.assertIn("openCommandPalette()", html)

    def test_keyboard_shortcuts_and_accessibility(self):
        resp = self.client.get("/")
        html = resp.text
        self.assertIn("e.key === 'k'", html)
        self.assertIn("e.key === 'Escape'", html)
        self.assertIn("e.key === 'n'", html)
        self.assertIn("<header", html)
        self.assertIn("<main", html)

if __name__ == "__main__":
    unittest.main()
