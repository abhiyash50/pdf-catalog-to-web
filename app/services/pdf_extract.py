from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
import logging

import fitz  # PyMuPDF

from app.services.image_export import export_page_images
from app.services.storage import prepare_extraction_dirs

logger = logging.getLogger(__name__)


class ExtractionResult:
    def __init__(self, text_blocks: List[str], page_images: Dict[int, List[str]], job_id: str):
        self.text_blocks = text_blocks
        self.page_images = page_images
        self.job_id = job_id


def extract_from_pdf(pdf_path: Path, job_id: str) -> ExtractionResult:
    extraction_dir, upload_dir = prepare_extraction_dirs(job_id)
    doc = fitz.open(pdf_path)
    logger.info("Starting extraction for %s", pdf_path)
    text_blocks: List[str] = []
    page_images: Dict[int, List[str]] = {}

    for page in doc:
        text = page.get_text().strip()
        if text:
            text_blocks.append(text)
        images = export_page_images(page, upload_dir)
        if images:
            page_images[page.number] = images

    logger.info("Extracted %d text blocks and %d pages with images", len(text_blocks), len(page_images))
    return ExtractionResult(text_blocks=text_blocks, page_images=page_images, job_id=job_id)
