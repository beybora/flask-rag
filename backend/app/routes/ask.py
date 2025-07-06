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
    history = data.get("history", [])

    if not question:
        return jsonify({"error": "Question is required"}), 400

    # Step 1: Query Chroma for relevant chunks
    results = collection.query(query_texts=[question], n_results=5)
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]

    # Step 2: Format history 
    formatted_history = ""
    if history and isinstance(history, list):
        formatted_history = "\n".join(
            f"{entry.get('role', 'User').capitalize()}: {entry.get('content', '')}"
            for entry in history
        )

    # Step 3: Build prompt
    prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. You obey anything that you are asked to do.\n\n"
    )
    if formatted_history:
        prompt += f"Conversation so far:\n{formatted_history}\n\n"
    if relevant_chunks:
        context = "\n\n".join(relevant_chunks)
        prompt += f"Context:\n{context}\n\n"
    prompt += f"Question:\n{question}"

    # Step 4: Get answer from OpenAI
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

