from __future__ import annotations

from typing import Any, Dict, List

from app.db import get_connection, serialize, deserialize


def add_knowledge(doc: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO knowledge (id, title, payload) VALUES (?, ?, ?)",
        (str(doc.get("id") or doc.get("title")), str(doc.get("title", "Untitled")), serialize(doc)),
    )
    conn.commit()
    conn.close()
    return doc


def list_knowledge() -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT id, title, payload FROM knowledge ORDER BY title").fetchall()
    conn.close()
    return [deserialize(row["payload"]) for row in rows]


def search_knowledge(topic: str = "", pattern: str = "") -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT payload FROM knowledge").fetchall()
    conn.close()

    matches: List[Dict[str, Any]] = []
    for row in rows:
        doc = deserialize(row["payload"])
        if topic and str(doc.get("topic", "")).lower() != topic.lower():
            continue
        if pattern and str(doc.get("pattern", "")).lower() != pattern.lower():
            continue
        matches.append(doc)
    return matches
