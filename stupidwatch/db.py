import sqlite3
from pathlib import Path
from typing import Final, List, Optional
from dataclasses import dataclass


class Settings:
    DB_PATH: Final[Path] = Path.home() / ".local" / "share" / "stupidwatch" / "data.db"


@dataclass
class Session:
    name: str
    total_seconds: float


class SessionRepository:
    @staticmethod
    def get_connection() -> sqlite3.Connection:
        Settings.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(Settings.DB_PATH)
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                name TEXT PRIMARY KEY,
                total_seconds REAL NOT NULL
            )
            """
        )
        return connection

    @staticmethod
    def add_time(session_name: str, seconds: float) -> None:
        conn = SessionRepository.get_connection()
        cur = conn.cursor()

        cur.execute("SELECT total_seconds FROM sessions WHERE name=?", (session_name,))
        row = cur.fetchone()

        if row:
            total = row[0] + seconds
            cur.execute(
                "UPDATE sessions SET total_seconds=? WHERE name=?",
                (total, session_name),
            )
        else:
            cur.execute(
                "INSERT INTO sessions (name, total_seconds) VALUES (?, ?)",
                (session_name, seconds),
            )

        conn.commit()
        conn.close()

    @staticmethod
    def list_sessions() -> List[Session]:
        conn = SessionRepository.get_connection()
        cur = conn.cursor()

        cur.execute("SELECT name, total_seconds FROM sessions")
        rows = cur.fetchall()

        conn.close()

        return [Session(name=row[0], total_seconds=row[1]) for row in rows]

    @staticmethod
    def get_session(session_name: str) -> Optional[Session]:
        conn = SessionRepository.get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT name, total_seconds FROM sessions WHERE name=?", (session_name,)
        )
        row = cur.fetchone()

        conn.close()

        if row:
            return Session(name=row[0], total_seconds=row[1])
        return None
