import shutil
from pathlib import Path

import fitz

from app.config import settings
from app.services.image_export import render_page_preview
from app.services.storage import ensure_directories


def test_render_page_preview_creates_file(tmp_path: Path):
    ensure_directories()
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello catalog")

    job_id = "testrender"
    output_dir = settings.upload_static_dir / job_id
    if output_dir.exists():
        shutil.rmtree(output_dir)

    result = render_page_preview(page, job_id, output_dir, scale=1.5, fmt="png")

    assert result.web_path.startswith("/static/uploads/")
    assert result.file_path.exists()

    # cleanup
    shutil.rmtree(output_dir, ignore_errors=True)
