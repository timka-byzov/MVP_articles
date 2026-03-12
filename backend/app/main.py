from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import create_db_and_tables
from app.api.auth import get_auth_router
from app.api import feed, articles, preferences

app = FastAPI(
    title="MVP Articles API",
    version="1.0.0",
    description="Персональная лента научных статей"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(get_auth_router(), prefix="/auth")
app.include_router(feed.router)
app.include_router(articles.router)
app.include_router(preferences.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {
        "message": "MVP Articles API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}