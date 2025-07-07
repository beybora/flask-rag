# tests/conftest.py
import os
import sys
import pytest

# Root-Verzeichnis zum Systempfad hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  

@pytest.fixture
def app():
    return create_app()
