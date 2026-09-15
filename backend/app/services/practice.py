from __future__ import annotations

from typing import Any, Dict, List


def build_practice_plan(email: str, number_of_problems: int = 3, topic: str = "Dynamic Programming") -> Dict[str, Any]:
    topics = ["Dynamic Programming", "Binary Search", "Graphs"]
    problems = [
        "Climbing Stairs",
        "Maximum Subarray",
        "Course Schedule",
        "Binary Search Tree Validation",
        "Word Ladder",
    ]
    return {
        "email": email,
        "focus_topics": ", ".join(topics[:2]),
        "target_difficulty": "Medium",
        "number_of_problems": number_of_problems,
        "problems": problems[:number_of_problems],
        "topic": topic,
    }
