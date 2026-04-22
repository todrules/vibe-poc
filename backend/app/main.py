"""FastAPI application entrypoint.

Startup sequence
----------------
1. Configure structured logging.
2. Validate required environment variables (fail fast via ``get_settings()``).
3. Register CORS middleware.
4. Mount API routers.
"""

import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.generate import router as generate_router
from app.core.config import get_settings

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifespan (startup / shutdown)
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler.

    Validates that all required environment variables are present at startup
    so the process fails immediately with a clear error rather than at the
    first request.

    Yields:
        Control to FastAPI while the application is running.

    Raises:
        KeyError: If any required environment variable is missing.
    """
    logger.info("Starting up — validating configuration.")
    get_settings()  # Raises KeyError early if env vars are absent.
    logger.info("Configuration valid. Application ready.")
    yield
    logger.info("Shutting down.")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Vibe POC API",
    version="0.1.0",
    description=(
        "Accepts requirement text and returns structured acceptance criteria, "
        "agent prompts, user stories, and test cases via OptnAI."
    ),
    lifespan=lifespan,
)

# Allow the Next.js dev server and any deployed frontend origin.
# Restrict ``allow_origins`` to known domains in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(generate_router)


@app.get("/healthz", tags=["health"])
def healthz() -> dict[str, str]:
    """Liveness probe endpoint for container orchestration health checks."""
    return {"status": "ok"}
