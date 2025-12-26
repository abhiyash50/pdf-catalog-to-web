from __future__ import annotations

import logging
import re
from typing import Dict, List, Optional, Sequence, Tuple, Union

from app.models import Product

logger = logging.getLogger(__name__)

PRICE_PATTERN = re.compile(
    r"(?i)(?:rs\.?|inr|₹|¥|円|usd|eur|cad|aud|\$|€)?\s*([0-9]+(?:[, ]?[0-9]{3})*(?:\.[0-9]{1,2})?)"
)


def extract_price(text: str) -> Optional[str]:
    match = PRICE_PATTERN.search(text)
    if match:
        return match.group(0).strip()
    return None


def _extract_lines(text: str) -> List[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    logger.debug("Split text into %d lines", len(lines))
    return lines


def _extract_specs(lines: Sequence[str]) -> List[Tuple[str, str]]:
    specs: List[Tuple[str, str]] = []
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key and value:
                specs.append((key, value))
    return specs


def parse_products(
    text_blocks: Sequence[Union[str, Tuple[int, str]]],
    page_images: Dict[int, List[str]],
    page_previews: Dict[int, str],
) -> List[Product]:
    products: List[Product] = []

    for idx, block in enumerate(text_blocks):
        if isinstance(block, tuple):
            page_number, text = block
        else:
            page_number, text = idx + 1, block

        lines = _extract_lines(text)
        name = lines[0] if lines else f"Page {page_number}"
        description = text.strip()
        price = extract_price(text)
        embedded_images = page_images.get(page_number, []) or None
        page_preview_url = page_previews.get(page_number)
        page_image_url = page_preview_url or (embedded_images[0] if embedded_images else None)
        specs = _extract_specs(lines)

        if not page_image_url:
            logger.warning("Missing page render for page %s", page_number)
            continue

        products.append(
            Product(
                name=name or f"Page {page_number}",
                description=description or "",
                page_number=page_number,
                page_image_url=page_image_url,
                extracted_text=description or None,
                price=price,
                image_url=page_image_url,
                page_preview_url=page_preview_url,
                specs=specs or None,
                embedded_images=embedded_images,
            )
        )

    logger.info("Parsed %d products", len(products))
    return products


__all__ = [
    "PRICE_PATTERN",
    "extract_price",
    "parse_products",
]
