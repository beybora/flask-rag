import io
import os
import pytest
from app import create_app
from reportlab.pdfgen import canvas
import tempfile

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_upload_txt_file_success(client):
    # Simulate a .txt file in memory
    data = {
        "file": (io.BytesIO(b"Test content"), "test.txt")
    }
    response = client.post("/api/upload/file", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "message" in json_data
    assert json_data["message"] == "File uploaded successfully"
    assert json_data["filename"] == "test.txt"

def test_upload_pdf_file_success(client):
    # Create a real PDF file in memory using reportlab
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)
    c.drawString(100, 750, "Hello PDF")
    c.save()
    pdf_buffer.seek(0)
    data = {
        "file": (pdf_buffer, "test.pdf")
    }
    response = client.post("/api/upload/file", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "message" in json_data
    assert json_data["message"] == "File uploaded successfully"
    assert json_data["filename"] == "test.pdf"

def test_upload_no_file(client):
    response = client.post("/api/upload/file", data={}, content_type="multipart/form-data")
    assert response.status_code == 400
    assert response.get_json()["error"] == "No file part"

def test_upload_empty_file(client):
    data = {
        "file": (io.BytesIO(b""), "")
    }
    response = client.post("/api/upload/file", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    assert response.get_json()["error"] == "No selected file"

def test_upload_wrong_filetype(client):
    data = {
        "file": (io.BytesIO(b"PNG content"), "image.png")
    }
    response = client.post("/api/upload/file", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    assert "Only .txt and .pdf files allowed" in response.get_json()["error"]
