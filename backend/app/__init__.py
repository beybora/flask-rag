from flask import Flask
from flask_cors import CORS
from app.routes.upload import upload_bp
from app.routes.ask import ask_bp
from app.routes.ask_ext import ask_ext_bp
import os

def create_app():
    app = Flask(__name__)
    
    # initialize cors
    CORS(app)

    # Ensure upload folder exists
    os.makedirs("uploads", exist_ok=True)

    # Register routes
    app.register_blueprint(upload_bp, url_prefix="/api/upload")
    app.register_blueprint(ask_bp, url_prefix="/api")
    app.register_blueprint(ask_ext_bp, url_prefix="/api")

    return app
