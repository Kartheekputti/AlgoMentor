from fastapi import APIRouter

from app.schemas import ChatMessage, ChatResponse
from app.services.agent import generate_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(chat_message: ChatMessage):
    return generate_response(chat_message)
