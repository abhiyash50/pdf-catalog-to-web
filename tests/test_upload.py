import fitz
from fastapi.testclient import TestClient

from app.main import app


def create_pdf_bytes(text: str) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    return doc.tobytes()


def test_upload_endpoint_processes_pdf():
    client = TestClient(app)
    pdf_bytes = create_pdf_bytes("Sample Product\nPrice ¥12,000")
    response = client.post(
        "/upload",
        files={"file": ("sample.pdf", pdf_bytes, "application/pdf")},
    )

    assert response.status_code == 200
    assert "Catalog Pages" in response.text
    assert "Sample Product" in response.text
