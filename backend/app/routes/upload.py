from flask import Blueprint, request, jsonify
from app.core.processor import process_uploaded_file
import os

upload_bp = Blueprint("upload", __name__)

# Folder where uploaded files will be stored
UPLOAD_FOLDER = "uploads"

@upload_bp.route("/file", methods=["POST"])
def upload_file():
    print("test")
    # Check if the request contains a file
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    mimetype = file.mimetype

    # Reject if no file is selected
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Only allow .txt and .pdf files
    if not (file.filename.endswith(".txt") or file.filename.endswith(".pdf")):
        return jsonify({"error": "Only .txt and .pdf files allowed"}), 400
    if not (mimetype == "text/plain" or mimetype == "application/pdf"):
        return jsonify({"error": "Only .txt and .pdf files allowed (mimetype)"}), 400

    # Save the uploaded file to the uploads folder
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    process_uploaded_file(save_path, mimetype)
    os.remove(save_path)

    return jsonify({
        "filename": file.filename,
        "message": "File uploaded successfully"
    })
