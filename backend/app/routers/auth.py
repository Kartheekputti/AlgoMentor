from fastapi import APIRouter, HTTPException, status

from app.schemas import TokenResponse, UserLogin, UserRegister
from app.services.auth import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(user: UserRegister):
    try:
        register_user(user.username, user.email, user.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    token = "demo-token-for-" + user.email
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    authenticated = authenticate_user(user.email, user.password)
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = "demo-token-for-" + user.email
    return TokenResponse(access_token=token)
