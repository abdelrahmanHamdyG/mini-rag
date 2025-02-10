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

def get_settings():
    return Settings()
