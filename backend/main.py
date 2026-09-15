from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.routers.health import router as health_router
from app.routers.knowledge import router as knowledge_router
from app.routers.progress import router as progress_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Personalized Agentic RAG Platform for DSA Preparation",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(knowledge_router)
app.include_router(progress_router)
app.include_router(chat_router)


@app.get("/")
def read_root():
    return {"message": "AlgoMentor API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.app_port, reload=True)
