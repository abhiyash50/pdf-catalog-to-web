from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import fitz  # PyMuPDF


@dataclass
class ExportedImage:
    file_path: Path
    web_path: str


def build_web_image_path(job_id: str, filename: str) -> str:
    """Create a URL path for an extracted image under the static uploads folder."""

    clean_name = Path(filename).name
    return f"/static/uploads/{job_id}/{clean_name}".replace("\\", "/")


def export_page_images(page: fitz.Page, job_id: str, output_dir: Path) -> List[ExportedImage]:
    """Export images from a page to the output directory.

    Returns list of ExportedImage entries with filesystem and web paths.
    """

    image_paths: List[ExportedImage] = []
    output_dir.mkdir(parents=True, exist_ok=True)
    images = page.get_images(full=True)
    if not images:
        return image_paths

    for idx, img in enumerate(images, start=1):
        xref = img[0]
        pix = fitz.Pixmap(page.parent, xref)
        if pix.n - pix.alpha >= 4:  # CMYK or similar; convert to RGB
            pix = fitz.Pixmap(fitz.csRGB, pix)
        image_name = f"page{page.number + 1}_img{idx}.png"
        output_path = output_dir / image_name
        pix.save(output_path)
        image_paths.append(
            ExportedImage(file_path=output_path.resolve(), web_path=build_web_image_path(job_id, image_name))
        )
        pix = None
    return image_paths
