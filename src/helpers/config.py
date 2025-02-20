import os
import ast
from dotenv import load_dotenv
from pathlib import Path

# Load the .env file from the project root
BASE_DIR = Path(__file__).resolve().parent.parent  # Adjust based on location
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings:
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME", "mini-RAG")
        self.APP_VERSION = os.getenv("APP_VERSION", "0.1")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        
        allowed_types_str = os.getenv("FILE_ALLOWED_TYPES", "['text/plain', 'application/pdf']")
        self.FILE_ALLOWED_TYPES = ast.literal_eval(allowed_types_str) if allowed_types_str else []
        self.FILE_MAX_SIZE = int(os.getenv("FILE_MAX_SIZE", 10))
        self.MONGO_URL=os.getenv("MONGO_URL", "")
        self.MONGO_DATABASE=os.getenv("MONGO_DATABASE", "")
        self.GENERATION_BACKEND = os.getenv("GENERATION_BACKEND", "OPENAI")
        self.EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "COHERE")

        self.OPENAI_API_URL = os.getenv("OPENAI_API_URL", "")
        self.COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")

        self.GENERATION_MODEL_ID = os.getenv("GENERATION_MODEL_ID", "gpt-3.5-turbo-0125")
        self.EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID", "embed-multilingual-light-v3.0")
        self.EMBEDDING_MODEL_SIZE = int(os.getenv("EMBEDDING_MODEL_SIZE", 384))

        
        self.VECTOR_DB_BACKEND = os.getenv("VECTOR_DB_BACKEND", "QDRANT")
        self.VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "qdrant_db")
        self.VECTOR_DB_DISTANCE = os.getenv("VECTOR_DB_DISTANCE", "COSINE")




def get_settings():
    return Settings()
