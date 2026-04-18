"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.api.routes.generate import router as generate_router

app = FastAPI(title="Vibe POC API")
app.include_router(generate_router)
