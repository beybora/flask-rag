import pytest
from flask import Flask
from unittest.mock import patch


def test_ask_route_returns_answer(client):
    dummy_question = "What is AI?"
    dummy_response = "AI stands for Artificial Intelligence."

    with patch("app.routes.ask.collection.query") as mock_query, \
         patch("app.routes.ask.client.chat.completions.create") as mock_chat:
        
        mock_query.return_value = {
            "documents": [["AI is the simulation of human intelligence by machines."]]
        }

        mock_chat.return_value = type("Response", (), {
            "choices": [type("Choice", (), {
                "message": type("Message", (), {
                    "content": dummy_response
                })()
            })()]
        })()

        res = client.post("/api/ask", json={"question": dummy_question, "history": []})
        assert res.status_code == 200
        assert res.get_json()["answer"] == dummy_response

def test_ask_route_missing_question(client):
    res = client.post("/api/ask", json={})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_reset_chroma_deletes_all(client):
    with patch("app.routes.ask.collection.get") as mock_get, \
         patch("app.routes.ask.collection.delete") as mock_delete:

        mock_get.return_value = {"ids": ["doc1", "doc2"]}
        res = client.post("/api/reset-chroma")

        assert res.status_code == 200
        data = res.get_json()
        assert data["status"] == "ok"
        assert data["deleted_count"] == 2
        mock_delete.assert_called_once_with(ids=["doc1", "doc2"])
