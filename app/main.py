from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.logging_conf import configure_logging
from app.routers import catalog

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

app.state.templates = Jinja2Templates(directory=str(settings.template_dir))
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
app.include_router(catalog.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error("Validation error: %s", exc)
    template = app.state.templates
    return template.TemplateResponse(
        "error.html",
        {"request": request, "message": "Invalid input provided."},
        status_code=400,
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    template = app.state.templates
    return template.TemplateResponse(
        "error.html",
        {"request": request, "message": "An unexpected error occurred."},
        status_code=500,
    )


@app.get("/health")
async def health_check():
    return {"status": "ok"}
