from flask import Blueprint, request, jsonify
from app.core.chroma import collection
from app.utils.embedding import get_openai_embedding
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ask_bp = Blueprint("ask", __name__)

@ask_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question is required"}), 400

    # Step 1: Query Chroma for relevant chunks
    results = collection.query(query_texts=[question], n_results=5)
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]

    if not relevant_chunks:
        return jsonify({"answer": "No relevant context found."})

    # Step 2: Generate prompt with context
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the answer concise."
        "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
    )

    # Step 3: Get answer from OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question},
            ],
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Reset Chroma 
@ask_bp.route("/reset-chroma", methods=["POST"])
def reset_chroma():
    try:
        all_docs = collection.get()
        ids = all_docs["ids"]

        if ids:
            collection.delete(ids=ids)

        return jsonify({"status": "ok", "deleted_count": len(ids)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

