from __future__ import annotations

from typing import Dict, Optional

from app.db import execute_write, fetch_one


def register_user(username: str, email: str, password: str) -> Dict[str, str]:
    normalized_email = email.strip().lower()
    if len(username.strip()) < 3:
        raise ValueError("Username must be at least 3 characters")
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters")

    existing = fetch_one("SELECT email FROM users WHERE email = ?", (normalized_email,))
    if existing:
        raise ValueError("User already exists")

    execute_write(
        "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
        (normalized_email, username.strip(), password),
    )
    return {"username": username.strip(), "email": normalized_email}


def authenticate_user(email: str, password: str) -> Optional[Dict[str, str]]:
    normalized_email = email.strip().lower()
    row = fetch_one(
        "SELECT username, email, password FROM users WHERE email = ?",
        (normalized_email,),
    )
    if not row:
        return None
    if row["password"] != password:
        return None
    return {"username": row["username"], "email": row["email"]}
