from unittest.mock import patch, MagicMock
from app.utils.embedding import get_openai_embedding

def test_get_openai_embedding_mock():
    fake_embedding = [0.1, 0.2, 0.3]
    with patch('app.utils.embedding.client') as mock_client:
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=fake_embedding)]
        mock_client.embeddings.create.return_value = mock_response
        result = get_openai_embedding("test text")
        assert result == fake_embedding
        mock_client.embeddings.create.assert_called_once() 