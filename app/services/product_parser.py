from __future__ import annotations

import logging
import re
from typing import Dict, List, Optional, Sequence, Tuple, Union

from app.models import Product

logger = logging.getLogger(__name__)

PRICE_PATTERN = re.compile(
    r"(?i)(?:rs\.?|inr|₹|¥|円|usd|eur|cad|aud|\$|€)?\s*([0-9]+(?:[, ]?[0-9]{3})*(?:\.[0-9]{1,2})?)"
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


def parse_products(
    text_blocks: Sequence[Union[str, Tuple[int, str]]],
    page_images: Dict[int, List[str]],
) -> List[Product]:
    products: List[Product] = []

    for idx, block in enumerate(text_blocks):
        if isinstance(block, tuple):
            page_number, text = block
        else:
            page_number, text = idx + 1, block

        paragraphs = split_text_into_blocks(text)
        name = paragraphs[0] if paragraphs else f"Page {page_number}"
        description = " ".join(paragraphs[1:]) if len(paragraphs) > 1 else ""
        description = description[:600]
        price = extract_price(text)
        images = page_images.get(page_number, [])
        image_path = images[0] if images else None

        products.append(
            Product(
                name=name or f"Page {page_number}",
                description=description or "",
                price=price,
                image_path=image_path,
            )
        )

    logger.info("Parsed %d products", len(products))
    return products


__all__ = [
    "PRICE_PATTERN",
    "split_text_into_blocks",
    "extract_price",
    "parse_products",
]
