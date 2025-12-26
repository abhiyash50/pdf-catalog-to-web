from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Product:
    name: str
    description: str
    page_number: int
    page_image_url: str
    extracted_text: Optional[str] = None
    price: Optional[str] = None
    image_url: Optional[str] = None
    page_preview_url: Optional[str] = None
    specs: Optional[List[Tuple[str, str]]] = None
    embedded_images: Optional[List[str]] = None
