from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import fitz  # PyMuPDF


@dataclass
class ExportedImage:
    file_path: Path
    web_path: str


def build_web_image_path(job_id: str, filename: str) -> str:
    """Create a URL path for an extracted image under the static uploads folder."""

    clean_name = Path(filename)
    # Ensure path separators are URL-safe forward slashes
    return f"/static/uploads/{job_id}/{clean_name.as_posix()}".replace("\\", "/")


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
        image_path = _export_original_image(page, xref, output_dir, idx)
        if image_path is None:
            # Fallback to pixmap rendering if the original cannot be extracted
            pix = fitz.Pixmap(page.parent, xref)
            if pix.n - pix.alpha >= 4:  # CMYK or similar; convert to RGB
                pix = fitz.Pixmap(fitz.csRGB, pix)
            image_path = output_dir / f"page{page.number + 1}_img{idx}.png"
            pix.save(image_path)
            pix = None

        image_paths.append(
            ExportedImage(
                file_path=image_path.resolve(),
                web_path=build_web_image_path(job_id, image_path.name),
            )
        )
    return image_paths


def _export_original_image(page: fitz.Page, xref: int, output_dir: Path, idx: int) -> Optional[Path]:
    """Attempt to extract and persist the original embedded image bytes."""

    try:
        image_dict = page.parent.extract_image(xref)
    except Exception:
        return None

    if not image_dict or "image" not in image_dict:
        return None

    ext = image_dict.get("ext", "png") or "png"
    image_bytes = image_dict["image"]
    output_path = output_dir / f"page{page.number + 1}_img{idx}.{ext}"
    output_path.write_bytes(image_bytes)
    return output_path


def render_page_preview(
    page: fitz.Page, job_id: str, output_dir: Path, scale: float = 2.0
) -> ExportedImage:
    """Render a high-resolution PNG preview for a given page."""

    pages_dir = output_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    matrix = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    filename = f"page_{page.number + 1}.png"
    file_path = pages_dir / filename
    pix.save(file_path)
    pix = None
    web_path = build_web_image_path(job_id, f"pages/{filename}")
    return ExportedImage(file_path=file_path.resolve(), web_path=web_path)
