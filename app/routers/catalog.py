from __future__ import annotations

import logging

from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import HTMLResponse

from app.config import settings
from app.services import pdf_extract, product_parser, storage

router = APIRouter()
logger = logging.getLogger(__name__)


def _validate_pdf(file: UploadFile) -> str:
    allowed_types = {"application/pdf", "application/x-pdf", "application/octet-stream"}
    filename = file.filename or ""
    if file.content_type not in allowed_types and not filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are allowed.")
    return filename or "upload.pdf"


def _too_large(size: int) -> bool:
    return size > settings.max_upload_size_bytes


@router.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return request.app.state.templates.TemplateResponse(
        "upload.html", {"request": request, "max_size_mb": settings.max_upload_size_mb}
    )


@router.post("/upload", response_class=HTMLResponse)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    template = request.app.state.templates
    job_id = None
    try:
        filename = _validate_pdf(file)
        file_bytes = await file.read()
        if not file_bytes:
            raise ValueError("Uploaded file is empty.")
        if _too_large(len(file_bytes)):
            return template.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "message": f"File exceeds maximum size of {settings.max_upload_size_mb} MB.",
                },
                status_code=413,
            )

        pdf_path, job_id = storage.save_upload(file_bytes, filename)
        extraction = pdf_extract.extract_from_pdf(pdf_path, job_id)
        products = product_parser.parse_products(extraction.text_blocks, extraction.page_images)

        return template.TemplateResponse(
            "results.html",
            {"request": request, "products": products, "job_id": job_id},
        )
    except ValueError as exc:
        logger.exception("Validation error while uploading PDF")
        return template.TemplateResponse(
            "error.html",
            {"request": request, "message": str(exc)},
            status_code=400,
        )
    except Exception:
        logger.exception("Error processing PDF upload")
        if job_id:
            storage.cleanup_job(job_id)
        return template.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": "Failed to process the PDF. Please try again with a valid file.",
            },
            status_code=500,
        )
