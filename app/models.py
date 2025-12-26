from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    name: str
    description: str
    price: Optional[str] = None
    image_path: Optional[str] = None
