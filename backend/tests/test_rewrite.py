import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_rewrite_chunk(client):
    chunk = "This is a long and complicated sentence that could be clearer."
    response = client.post("/api/chunks/rewrite", json={"chunk": chunk})
    assert response.status_code == 200
    data = response.get_json()
    assert "rewritten" in data
    assert data["rewritten"] != chunk 