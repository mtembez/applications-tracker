"""Database persistence layer using SQLite with WAL mode and foreign key constraints."""
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

from .models import ApplicationCreate, AppStatus, LocationType, EventType

DEFAULT_DB_DIR = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "apptracker"
DEFAULT_DB_PATH = Path(os.environ.get("APP_TRACKER_DB", DEFAULT_DB_DIR / "applications.db"))

def get_db_path() -> Path:
    db_path = Path(os.environ.get("APP_TRACKER_DB", DEFAULT_DB_PATH))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path

def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    target_path = db_path or get_db_path()
    conn = sqlite3.connect(str(target_path), timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn

def init_db(db_path: Optional[Path] = None) -> None:
    conn = get_connection(db_path)
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL COLLATE NOCASE,
                    role TEXT NOT NULL,
                    location_type TEXT NOT NULL,
                    compensation TEXT,
                    channel TEXT NOT NULL,
                    status TEXT NOT NULL,
                    job_url TEXT,
                    contact_person TEXT,
                    notes TEXT,
                    applied_at TEXT NOT NULL,
                    last_activity_at TEXT NOT NULL
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS timeline_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_id INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    details TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (app_id) REFERENCES applications (id) ON DELETE CASCADE
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_apps_status ON applications(status);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_apps_company ON applications(company);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_timeline_appid ON timeline_events(app_id);")
    finally:
        conn.close()

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def create_application(app: ApplicationCreate, db_path: Optional[Path] = None) -> int:
    conn = get_connection(db_path)
    now = _now_iso()
    try:
        with conn:
            cursor = conn.execute("""
                INSERT INTO applications (
                    company, role, location_type, compensation, channel,
                    status, job_url, contact_person, notes, applied_at, last_activity_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                app.company, app.role, app.location_type.value, app.compensation,
                app.channel, app.status.value, app.job_url, app.contact_person,
                app.notes, now, now
            ))
            app_id = cursor.lastrowid
            conn.execute("""
                INSERT INTO timeline_events (app_id, event_type, details, created_at)
                VALUES (?, ?, ?, ?)
            """, (app_id, EventType.CREATED.value, f"Application recorded with status {app.status.value}", now))
            return app_id
    finally:
        conn.close()

def update_status(app_id: int, new_status: AppStatus, note: Optional[str] = None, db_path: Optional[Path] = None) -> bool:
    conn = get_connection(db_path)
    now = _now_iso()
    try:
        with conn:
            cursor = conn.execute("SELECT status FROM applications WHERE id = ?", (app_id,))
            row = cursor.fetchone()
            if not row:
                return False
            old_status = row["status"]
            conn.execute("""
                UPDATE applications
                SET status = ?, last_activity_at = ?
                WHERE id = ?
            """, (new_status.value, now, app_id))
            detail = f"Status transitioned: {old_status} -> {new_status.value}"
            if note:
                detail += f" | Note: {note}"
            conn.execute("""
                INSERT INTO timeline_events (app_id, event_type, details, created_at)
                VALUES (?, ?, ?, ?)
            """, (app_id, EventType.STATUS_CHANGE.value, detail, now))
            return True
    finally:
        conn.close()

def add_event(app_id: int, event_type: EventType, details: str, db_path: Optional[Path] = None) -> bool:
    conn = get_connection(db_path)
    now = _now_iso()
    try:
        with conn:
            cursor = conn.execute("SELECT id FROM applications WHERE id = ?", (app_id,))
            if not cursor.fetchone():
                return False
            conn.execute("""
                INSERT INTO timeline_events (app_id, event_type, details, created_at)
                VALUES (?, ?, ?, ?)
            """, (app_id, event_type.value, details, now))
            conn.execute("UPDATE applications SET last_activity_at = ? WHERE id = ?", (now, app_id))
            return True
    finally:
        conn.close()

def get_application(app_id: int, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    conn = get_connection(db_path)
    try:
        cursor = conn.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
        row = cursor.fetchone()
        if not row:
            return None
        data = dict(row)
        events_cursor = conn.execute(
            "SELECT * FROM timeline_events WHERE app_id = ? ORDER BY id ASC", (app_id,)
        )
        data["timeline"] = [dict(ev) for ev in events_cursor.fetchall()]
        return data
    finally:
        conn.close()

def list_applications(
    status: Optional[str] = None,
    search: Optional[str] = None,
    db_path: Optional[Path] = None
) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    try:
        query = "SELECT * FROM applications WHERE 1=1"
        params: list = []
        if status:
            query += " AND status = ?"
            params.append(status.upper())
        if search:
            query += " AND (company LIKE ? OR role LIKE ? OR channel LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term])
        query += " ORDER BY last_activity_at DESC"
        cursor = conn.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]
    finally:
        conn.close()

def delete_application(app_id: int, db_path: Optional[Path] = None) -> bool:
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
            return cursor.rowcount > 0
    finally:
        conn.close()

def get_metrics(db_path: Optional[Path] = None) -> Dict[str, Any]:
    conn = get_connection(db_path)
    try:
        cursor = conn.execute("SELECT status, COUNT(*) as cnt FROM applications GROUP BY status")
        funnel = {s.value: 0 for s in AppStatus}
        total = 0
        for row in cursor.fetchall():
            status_val = row["status"]
            count = row["cnt"]
            if status_val in funnel:
                funnel[status_val] = count
            total += count
    finally:
        conn.close()

    interviews = (
        funnel.get(AppStatus.SCREENING.value, 0) +
        funnel.get(AppStatus.TECHNICAL.value, 0) +
        funnel.get(AppStatus.FINAL_ROUND.value, 0) +
        funnel.get(AppStatus.OFFER.value, 0)
    )
    offers = funnel.get(AppStatus.OFFER.value, 0)
    rejections = funnel.get(AppStatus.REJECTED.value, 0)
    withdrawn = funnel.get(AppStatus.WITHDRAWN.value, 0)
    active = total - rejections - withdrawn

    interview_rate = (interviews / total * 100.0) if total > 0 else 0.0
    offer_rate = (offers / total * 100.0) if total > 0 else 0.0

    return {
        "total_applications": total,
        "active_applications": active,
        "interview_count": interviews,
        "offer_count": offers,
        "rejection_count": rejections,
        "interview_rate_pct": round(interview_rate, 1),
        "offer_rate_pct": round(offer_rate, 1),
        "funnel": funnel
    }
