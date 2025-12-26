from __future__ import annotations

import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_STATIC_DIR = BASE_DIR / "static"
DEFAULT_TEMPLATE_DIR = BASE_DIR / "templates"
DEFAULT_TMP_DIR = BASE_DIR.parent / "data" / "tmp"
DEFAULT_EXTRACTED_DIR = BASE_DIR.parent / "data" / "extracted"
DEFAULT_UPLOAD_DIR = DEFAULT_STATIC_DIR / "uploads"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field("pdf-catalog-to-web", validation_alias="APP_NAME")
    max_upload_mb: int = Field(25, validation_alias="MAX_UPLOAD_MB", description="Maximum upload size in megabytes")
    log_level: str = Field("INFO", validation_alias="LOG_LEVEL")
    env: str = Field("production", validation_alias="ENV")

    static_dir: Path = Field(default_factory=lambda: DEFAULT_STATIC_DIR)
    template_dir: Path = Field(default_factory=lambda: DEFAULT_TEMPLATE_DIR)
    tmp_dir: Path = Field(default_factory=lambda: DEFAULT_TMP_DIR, validation_alias="TMP_DIR")
    extracted_dir: Path = Field(default_factory=lambda: DEFAULT_EXTRACTED_DIR, validation_alias="EXTRACTED_DIR")
    upload_static_dir: Path = Field(default_factory=lambda: DEFAULT_UPLOAD_DIR, validation_alias="UPLOAD_DIR")

    @property
    def max_upload_size_mb(self) -> int:
        return self.max_upload_mb

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


settings = Settings()

# ensure directories exist at import time for convenience
for path in [settings.tmp_dir, settings.extracted_dir, settings.upload_static_dir]:
    try:
        os.makedirs(path, exist_ok=True)
    except OSError:
        # In restrictive environments, fail silently; service layer will raise as needed
        pass
