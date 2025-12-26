from __future__ import annotations

import logging
import re
from typing import Dict, List, Optional

from app.models import Product

logger = logging.getLogger(__name__)

PRICE_PATTERN = re.compile(
    r"(?i)(?:rs\.?|inr|₹|\$|€|usd)?\s*([0-9]{1,3}(?:[, ]?[0-9]{3})*(?:\.[0-9]{2})?)"
)


def split_text_into_blocks(text: str) -> List[str]:
    blocks = [block.strip() for block in re.split(r"\n{2,}", text) if block.strip()]
    logger.debug("Split text into %d blocks", len(blocks))
    return blocks


def extract_price(text: str) -> Optional[str]:
    match = PRICE_PATTERN.search(text)
    if match:
        return match.group(0).strip()
    return None


def parse_products(text_blocks: List[str], page_images: Dict[int, List[str]]) -> List[Product]:
    products: List[Product] = []
    image_lookup = _flatten_images(page_images)
    image_iter = iter(image_lookup)

    for block in text_blocks:
        paragraphs = split_text_into_blocks(block)
        if not paragraphs:
            continue
        name = paragraphs[0]
        description = " ".join(paragraphs[1:]) if len(paragraphs) > 1 else ""
        price = extract_price(block)
        try:
            image_path = next(image_iter)
        except StopIteration:
            image_path = None
        products.append(Product(name=name, description=description, price=price, image_path=image_path))

    logger.info("Parsed %d products", len(products))
    return products


def _flatten_images(page_images: Dict[int, List[str]]) -> List[str]:
    ordered_pages = sorted(page_images.keys())
    images: List[str] = []
    for page in ordered_pages:
        images.extend(page_images[page])
    return images


__all__ = [
    "PRICE_PATTERN",
    "split_text_into_blocks",
    "extract_price",
    "parse_products",
]
