from fastapi import FastAPI

from app.api import categories, news

app = FastAPI(title="Daily News Digest API")

app.include_router(news.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
