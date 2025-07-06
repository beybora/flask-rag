import os
from app.utils.text import split_text
from app.utils.embedding import get_openai_embedding
from app.core.chroma import collection

def process_uploaded_file(filepath):
    # Step 1: Load content from file
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Step 2: Split into chunks
    chunks = split_text(text)

    # Step 3: Get embeddings + insert
    for i, chunk in enumerate(chunks):
        emb = get_openai_embedding(chunk)
        doc_id = f"{os.path.basename(filepath)}_chunk{i+1}"
        collection.upsert(ids=[doc_id], documents=[chunk], embeddings=[emb])
