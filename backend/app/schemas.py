from __future__ import annotations

import re
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must include at least one lowercase letter")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must include at least one uppercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must include at least one number")
        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError("Password must include at least one special character")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1)
    mode: str = "concept"
    history: List[Dict[str, Any]] = []
    api_key: Optional[str] = None
    provider: Optional[str] = None
    user_email: Optional[str] = None
    language: Optional[str] = "python"
    hint_level: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    mode: str
    sources: list[str] = []
    pattern: Optional[str] = None
    hint_level: Optional[int] = None
    suggested_next_actions: List[str] = []
    similar_problems: List[Dict[str, Any]] = []

