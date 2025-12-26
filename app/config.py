from __future__ import annotations

import os
from pathlib import Path
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "pdf-catalog-to-web"
    max_upload_size_mb: int = Field(25, description="Maximum upload size in megabytes")
    static_dir: Path = Path(__file__).resolve().parent / "static"
    template_dir: Path = Path(__file__).resolve().parent / "templates"
    data_dir: Path = Path(__file__).resolve().parent.parent / "data"

    class Config:
        env_prefix = "APP_"
        case_sensitive = False

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def tmp_dir(self) -> Path:
        return self.data_dir / "tmp"

    @property
    def extracted_dir(self) -> Path:
        return self.data_dir / "extracted"

    @property
    def upload_static_dir(self) -> Path:
        return self.static_dir / "uploads"


settings = Settings()

# ensure directories exist at import time for convenience
for path in [settings.tmp_dir, settings.extracted_dir, settings.upload_static_dir]:
    try:
        os.makedirs(path, exist_ok=True)
    except OSError:
        # In restrictive environments, fail silently; service layer will raise as needed
        pass
