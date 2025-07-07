import os
from app.utils.text import split_text
from app.utils.embedding import get_openai_embedding
from app.core.chroma import collection
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    texts = [page.extract_text().strip() for page in reader.pages if page.extract_text()]
    return "\n\n".join(texts)

def process_uploaded_file(filepath, mimetype):
    if mimetype == "application/pdf":
        text = extract_text_from_pdf(filepath)
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    chunks = split_text(text)
    for i, chunk in enumerate(chunks):
        emb = get_openai_embedding(chunk)
        doc_id = f"{os.path.basename(filepath)}_chunk{i+1}"
        collection.upsert(ids=[doc_id], documents=[chunk], embeddings=[emb])
