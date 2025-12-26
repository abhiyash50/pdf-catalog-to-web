from __future__ import annotations

from pathlib import Path
from typing import List

import fitz  # PyMuPDF


def export_page_images(page: fitz.Page, output_dir: Path) -> List[str]:
    """Export images from a page to the output directory.

    Returns list of relative file names stored under static uploads directory.
    """
    image_paths: List[str] = []
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
        image_paths.append(str(output_path))
        pix = None
    return image_paths
