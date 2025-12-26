from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Product:
    name: str
    description: str
    price: Optional[str] = None
    image_url: Optional[str] = None
    page_preview_url: Optional[str] = None
    specs: Optional[List[Tuple[str, str]]] = None
