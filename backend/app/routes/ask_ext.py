from flask import Blueprint, request, jsonify
from app.core.chroma import collection
from app.core.mongo import prepared_chunks
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ask_ext_bp = Blueprint("ask_ext", __name__)

@ask_ext_bp.route("/ask/prepare", methods=["POST"])
def ask_prepare():
    data = request.get_json()
    question = data.get("question")
    session_id = data.get("session_id")
    if not question or not session_id:
        return jsonify({"error": "Missing question or session_id"}), 400

    results = collection.query(query_texts=[question], n_results=5)
    chunks = [doc for sublist in results["documents"] for doc in sublist]
    prepared_chunks.replace_one(
        {"session_id": session_id},
        {"session_id": session_id, "chunks": chunks, "question": question},
        upsert=True
    )
    return jsonify({"chunks": chunks})

@ask_ext_bp.route("/chunks/rewrite", methods=["POST"])
def rewrite_chunk():
    data = request.get_json()
    chunk = data.get("chunk")
    if not chunk:
        return jsonify({"error": "Missing chunk"}), 400
    prompt = f"Rewrite the following text to be clearer and more concise:\n\n{chunk}"
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=512,
        temperature=0.7,
    )
    rewritten = response.choices[0].text.strip()
    return jsonify({"rewritten": rewritten})

@ask_ext_bp.route("/ask/submit", methods=["POST"])
def ask_submit():
    data = request.get_json()
    session_id = data.get("session_id")
    question = data.get("question")
    chunks = data.get("chunks")
    if not question or not chunks:
        return jsonify({"error": "Missing question or chunks"}), 400

    prepared_chunks.delete_one({"session_id": session_id})

    context = "\n\n".join(chunks)
    prompt = (
        "You are an assistant for question-answering tasks. Use the following context to answer the question.\n\n"
        f"Context:\n{context}\n\nQuestion:\n{question}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ],
    )
    answer = response.choices[0].message.content
    return jsonify({"answer": answer}) 