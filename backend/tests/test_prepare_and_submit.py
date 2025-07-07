import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_prepare_and_submit(client):
    session_id = "test-session"
    question = "What is this document about?"
    # Prepare
    response = client.post("/api/ask/prepare", json={"question": question, "session_id": session_id})
    assert response.status_code == 200
    data = response.get_json()
    assert "chunks" in data
    assert isinstance(data["chunks"], list)
    # Submit
    submit = client.post("/api/ask/submit", json={
        "session_id": session_id,
        "question": question,
        "chunks": data["chunks"]
    })
    assert submit.status_code == 200
    submit_data = submit.get_json()
    assert "answer" in submit_data 