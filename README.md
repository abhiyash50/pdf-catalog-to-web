# PDF Catalog to Web

A FastAPI application that turns PDF product catalogs into a web-friendly gallery. Upload a PDF and view extracted products, images, and prices in a responsive grid.

## Features
- Upload PDF catalogs up to a configurable size (default 25MB)
- Extract text and images using PyMuPDF
- Parse products with price detection and associate nearby images
- Server-rendered pages via Jinja2 templates
- Docker and local development support

## Getting Started

### Prerequisites
- Python 3.11
- pip

### Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # on Windows use .venv\\Scripts\\activate
pip install -r requirements.txt
```

### Run the app
```bash
uvicorn app.main:app --reload
```
Visit http://localhost:8000 to upload a PDF.

### Configuration
Environment variables (prefixed with `APP_`):
- `APP_MAX_UPLOAD_SIZE_MB`: maximum upload size in MB (default 25)

### Docker
Build and run with Docker:
```bash
docker compose up --build
```
The service will be available at http://localhost:8000.

## Project Structure
- `app/main.py` – FastAPI entrypoint, routing, and template configuration
- `app/services/` – PDF extraction, storage, and product parsing helpers
- `app/templates/` – Jinja2 templates for upload, results, and error pages
- `app/static/` – CSS and exported images

## Testing
```bash
pytest
```

## Notes
- Extracted images are stored in `app/static/uploads/<job_id>/` and served via `/static/uploads/...`.
- Temporary uploads and extracted assets are created under `data/tmp` and `data/extracted` at runtime.
