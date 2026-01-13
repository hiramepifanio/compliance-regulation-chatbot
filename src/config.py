import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "models/embedding-001")
LLM_MODEL_NAME = os.getenv("LLM_MODEL", "gemini-3-flash-preview")
GROUNDING_THRESHOLD = float(os.getenv("GROUNDING_THRESHOLD", "0.5"))

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY must be set in the .env file.")
