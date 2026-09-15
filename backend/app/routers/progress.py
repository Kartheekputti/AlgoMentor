from fastapi import APIRouter

from app.services.progress import add_progress, get_progress_summary

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/summary")
def get_summary_route(email: str):
    return get_progress_summary(email)


@router.post("")
def add_progress_route(email: str, problem: dict):
    return add_progress(email, problem)
