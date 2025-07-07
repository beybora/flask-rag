import io
import pytest
from app import create_app

def create_pdf_bytes(text="Hello PDF world."):
    from reportlab.pdfgen import canvas
    import io
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)
    c.drawString(100, 750, text)
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_upload_txt_and_chunk(client):
    data = {"file": (io.BytesIO(b"Hello world. This is a test file."), "test.txt")}
    response = client.post("/api/upload/file", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert response.get_json()["message"] == "File uploaded successfully"

def test_upload_pdf_and_chunk(client):
    pdf_buffer = create_pdf_bytes()
    data = {"file": (pdf_buffer, "test.pdf")}
    response = client.post("/api/upload/file", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert response.get_json()["message"] == "File uploaded successfully" 