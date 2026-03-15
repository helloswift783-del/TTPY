from __future__ import annotations

import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path


class DatabaseManager:
    """Simple SQLite manager for study sessions, planner entries, and settings."""

    def __init__(self, db_path: str = "tt_py.db") -> None:
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                topic TEXT,
                duration_minutes INTEGER NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS planner_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_of_week INTEGER NOT NULL,
                subject TEXT NOT NULL,
                topic TEXT,
                target_hours REAL NOT NULL DEFAULT 1.0,
                slot_order INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        self.conn.commit()
        self._ensure_defaults()

    def _ensure_defaults(self) -> None:
        defaults = {
            "pomodoro_study_minutes": "25",
            "pomodoro_break_minutes": "5",
            "theme": "dark",
            "weekly_goal_hours": "20",
        }
        for key, value in defaults.items():
            self.set_setting_if_missing(key, value)

    def set_setting_if_missing(self, key: str, value: str) -> None:
        cur = self.conn.cursor()
        cur.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def get_setting(self, key: str, default: str = "") -> str:
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cur.fetchone()
        return row["value"] if row else default

    def set_setting(self, key: str, value: str) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
        self.conn.commit()

    def add_session(
        self,
        duration_minutes: int,
        started_at: datetime,
        ended_at: datetime,
        subject: str = "Focus Session",
        topic: str = "Pomodoro",
    ) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO study_sessions (subject, topic, duration_minutes, started_at, ended_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (subject, topic, duration_minutes, started_at.isoformat(), ended_at.isoformat()),
        )
        self.conn.commit()

    def get_total_hours_for_date(self, day: date) -> float:
        day_start = datetime.combine(day, datetime.min.time())
        day_end = day_start + timedelta(days=1)
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT COALESCE(SUM(duration_minutes), 0) as total_minutes
            FROM study_sessions
            WHERE started_at >= ? AND started_at < ?
            """,
            (day_start.isoformat(), day_end.isoformat()),
        )
        minutes = cur.fetchone()["total_minutes"]
        return round(minutes / 60.0, 2)

    def get_total_hours_range(self, start: date, end_exclusive: date) -> float:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT COALESCE(SUM(duration_minutes), 0) as total_minutes
            FROM study_sessions
            WHERE started_at >= ? AND started_at < ?
            """,
            (datetime.combine(start, datetime.min.time()).isoformat(), datetime.combine(end_exclusive, datetime.min.time()).isoformat()),
        )
        minutes = cur.fetchone()["total_minutes"]
        return round(minutes / 60.0, 2)

    def get_daily_hours_last_n_days(self, days: int = 30) -> list[tuple[str, float]]:
        today = date.today()
        output: list[tuple[str, float]] = []
        for i in range(days - 1, -1, -1):
            d = today - timedelta(days=i)
            output.append((d.strftime("%d %b"), self.get_total_hours_for_date(d)))
        return output

    def save_planner_entry(self, day_of_week: int, subject: str, topic: str, target_hours: float, slot_order: int) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO planner_entries (day_of_week, subject, topic, target_hours, slot_order)
            VALUES (?, ?, ?, ?, ?)
            """,
            (day_of_week, subject, topic, target_hours, slot_order),
        )
        self.conn.commit()

    def clear_planner(self) -> None:
        self.conn.execute("DELETE FROM planner_entries")
        self.conn.commit()

    def get_planner_entries(self) -> list[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT day_of_week, subject, topic, target_hours, slot_order
            FROM planner_entries
            ORDER BY day_of_week, slot_order
            """
        )
        return cur.fetchall()

    def get_study_streak(self) -> int:
        streak = 0
        current = date.today()
        while self.get_total_hours_for_date(current) > 0:
            streak += 1
            current -= timedelta(days=1)
        return streak
