from fastapi import APIRouter

from app.services.knowledge import add_knowledge, list_knowledge, search_knowledge

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("")
def get_knowledge():
    return {"items": list_knowledge()}


@router.post("")
def create_knowledge(doc: dict):
    return add_knowledge(doc)


@router.get("/search")
def search_knowledge_route(topic: str = "", pattern: str = ""):
    return {"items": search_knowledge(topic=topic, pattern=pattern)}
