import io
import os
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_upload_txt_file_success(client):
    # Simuliere eine .txt-Datei im Memory
    data = {
        "file": (io.BytesIO(b"Test content"), "test.txt")
    }
    response = client.post("/api/upload/file", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    json_data = response.get_json()
    assert "message" in json_data
    assert json_data["message"] == "File uploaded successfully"
    assert json_data["filename"] == "test.txt"

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
        "file": (io.BytesIO(b"PDF content"), "document.pdf")
    }
    response = client.post("/api/upload/file", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    assert response.get_json()["error"] == "Only .txt files allowed"
