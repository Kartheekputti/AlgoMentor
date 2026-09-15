import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "algomentor.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            problem_id TEXT,
            name TEXT,
            topic TEXT,
            difficulty TEXT,
            status TEXT,
            attempts INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS knowledge (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            payload TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


def fetch_one(query: str, params: tuple = ()):
    conn = get_connection()
    row = conn.execute(query, params).fetchone()
    conn.close()
    return row


def execute_write(query: str, params: tuple = ()):
    conn = get_connection()
    conn.execute(query, params)
    conn.commit()
    conn.close()


def serialize(value):
    return json.dumps(value, ensure_ascii=False)


def deserialize(value):
    if value is None:
        return {}
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {}
