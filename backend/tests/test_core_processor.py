from unittest.mock import patch, MagicMock
from app.core.processor import process_uploaded_file
import tempfile
import os

def test_process_uploaded_file_calls_embedding_and_upsert():
    fake_embedding = [0.1, 0.2, 0.3]
    fake_chunks = ["chunk1", "chunk2"]
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmp:
        tmp.write("abcdefghij")
        tmp_path = tmp.name
    with patch('app.core.processor.get_openai_embedding', return_value=fake_embedding) as mock_embed, \
         patch('app.core.processor.split_text', return_value=fake_chunks) as mock_split, \
         patch('app.core.processor.collection') as mock_collection:
        process_uploaded_file(tmp_path)
        # for each chunk an embedding and upsert
        assert mock_embed.call_count == len(fake_chunks)
        assert mock_collection.upsert.call_count == len(fake_chunks)
        # ids and documents
        for i, call in enumerate(mock_collection.upsert.call_args_list):
            args, kwargs = call
            assert kwargs['ids'] == [f"{os.path.basename(tmp_path)}_chunk{i+1}"]
            assert kwargs['documents'] == [fake_chunks[i]]
            assert kwargs['embeddings'] == [fake_embedding]
    os.remove(tmp_path) 