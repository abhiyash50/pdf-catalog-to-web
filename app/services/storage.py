from __future__ import annotations

import shutil
import uuid
from pathlib import Path
from typing import Tuple

from app.config import settings


def ensure_directories() -> None:
    for path in [settings.tmp_dir, settings.extracted_dir, settings.upload_static_dir]:
        path.mkdir(parents=True, exist_ok=True)


def save_upload(file_bytes: bytes, filename: str) -> Tuple[Path, str]:
    """Save uploaded PDF to tmp directory and return path and job id."""
    ensure_directories()
    job_id = uuid.uuid4().hex
    tmp_path = settings.tmp_dir / f"{job_id}_{filename}"
    tmp_path.write_bytes(file_bytes)
    return tmp_path, job_id


def prepare_extraction_dirs(job_id: str) -> Tuple[Path, Path]:
    """Return extraction output directories for text and images."""
    ensure_directories()
    extraction_dir = settings.extracted_dir / job_id
    upload_dir = settings.upload_static_dir / job_id
    extraction_dir.mkdir(parents=True, exist_ok=True)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return extraction_dir, upload_dir


def cleanup_job(job_id: str) -> None:
    extraction_dir = settings.extracted_dir / job_id
    upload_dir = settings.upload_static_dir / job_id
    if extraction_dir.exists():
        shutil.rmtree(extraction_dir, ignore_errors=True)
    if upload_dir.exists():
        shutil.rmtree(upload_dir, ignore_errors=True)
