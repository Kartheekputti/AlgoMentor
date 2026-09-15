from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List

from app.db import get_connection


def add_progress(email: str, problem: Dict[str, Any]) -> Dict[str, Any]:
    email = email.strip().lower()
    conn = get_connection()
    conn.execute(
        "INSERT INTO progress (email, problem_id, name, topic, difficulty, status, attempts) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            email,
            problem.get("problem_id"),
            problem.get("name"),
            problem.get("topic"),
            problem.get("difficulty"),
            problem.get("status"),
            problem.get("attempts", 0),
        ),
    )
    conn.commit()
    conn.close()
    return problem


def get_progress_summary(email: str) -> Dict[str, Any]:
    email = email.strip().lower()
    conn = get_connection()
    rows = conn.execute(
        "SELECT problem_id, name, topic, difficulty, status, attempts FROM progress WHERE email = ? ORDER BY created_at DESC",
        (email,),
    ).fetchall()
    conn.close()

    items = [dict(row) for row in rows]
    solved = [item for item in items if item.get("status") == "solved"]
    attempted = [item for item in items if item.get("status") == "attempted"]
    by_topic: Dict[str, int] = defaultdict(int)
    for item in items:
        topic = str(item.get("topic", "Unknown")).strip() or "Unknown"
        by_topic[topic] += 1

    weak_topics = sorted(by_topic.items(), key=lambda item: item[1])[:3]
    return {
        "solved_count": len(solved),
        "attempted_count": len(attempted),
        "total_problems": len(items),
        "weak_topics": [topic for topic, _ in weak_topics],
        "topic_distribution": dict(by_topic),
    }
