from __future__ import annotations

import logging
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.config import settings
from app.services import pdf_extract, product_parser, storage

router = APIRouter()
logger = logging.getLogger(__name__)


def _validate_pdf(file: UploadFile) -> None:
    if file.content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")


@router.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return request.app.state.templates.TemplateResponse(
        "upload.html", {"request": request, "max_size_mb": settings.max_upload_size_mb}
    )


@router.post("/upload", response_class=HTMLResponse)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    _validate_pdf(file)
    file_bytes = await file.read()
    if len(file_bytes) > settings.max_upload_size_bytes:
        raise HTTPException(status_code=413, detail="File too large.")

    pdf_path, job_id = storage.save_upload(file_bytes, file.filename)
    try:
        extraction = pdf_extract.extract_from_pdf(pdf_path, job_id)
        products = product_parser.parse_products(extraction.text_blocks, extraction.page_images)
    except Exception as exc:
        logger.exception("Error processing PDF")
        storage.cleanup_job(job_id)
        raise HTTPException(status_code=500, detail="Failed to process PDF") from exc

    uploads_root = settings.upload_static_dir
    for product in products:
        if product.image_path:
            product.image_path = "/static/" + str(Path(product.image_path).relative_to(settings.static_dir))

    return request.app.state.templates.TemplateResponse(
        "results.html",
        {"request": request, "products": products, "job_id": job_id},
    )
