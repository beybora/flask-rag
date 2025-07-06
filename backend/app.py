import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions

# === Step 0: Setup OpenAI + Chroma clients ===
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_key,
    model_name="text-embedding-3-small"
)

chroma_client = chromadb.PersistentClient(path="chroma_pa")
collection = chroma_client.get_or_create_collection(
    name="document_collection",
    embedding_function=openai_ef
)

client = OpenAI(api_key=openai_key)

# === Step 1: Load documents from folder ===
def load_documents_from_directory(directory_path):
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), "r", encoding="utf-8") as file:
                documents.append({"id": filename, "text": file.read()})
    return documents

# === Step 2: Split documents into chunks ===
def split_text(text, chunk_size=1000, chunk_overlap=20):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

# === Step 3: Create embeddings with OpenAI ===
def get_openai_embedding(text):
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding

# === Step 4: Insert chunks into Chroma ===
def insert_documents(documents):
    for doc in documents:
        doc["embedding"] = get_openai_embedding(doc["text"])
        collection.upsert(
            ids=[doc["id"]],
            documents=[doc["text"]],
            embeddings=[doc["embedding"]]
        )

# === Step 5: Query relevant chunks from Chroma ===
def query_documents(question, n_results=5):
    results = collection.query(query_texts=question, n_results=n_results)
    return [doc for sublist in results["documents"] for doc in sublist]

# === Step 6: Send context to OpenAI and get answer ===
def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the answer concise.\n\n"
        f"Context:\n{context}\n\nQuestion:\n{question}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ],
    )
    return response.choices[0].message

# Optional run (can be removed in API version)
# documents = load_documents_from_directory("./news_articles")
# chunked = [{"id": f"{doc['id']}_chunk{i+1}", "text": chunk}
#            for doc in documents
#            for i, chunk in enumerate(split_text(doc["text"]))]

# insert_documents(chunked)
# answer = generate_response("Tell me about databricks", query_documents("Tell me about databricks"))
# print(answer)
