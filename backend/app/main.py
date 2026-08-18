from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import categories, news
from app.core.config import settings

app = FastAPI(title="Daily News Digest API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(news.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
