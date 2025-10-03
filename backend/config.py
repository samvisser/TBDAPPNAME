"""
Configuration module for the backend application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in backend directory
backend_dir = Path(__file__).resolve().parent
env_path = backend_dir / '.env'
load_dotenv(env_path)

# Get API key from environment
API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True

# Gemini Configuration
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_TOKENS = 500
GEMINI_TOP_P = 0.8
GEMINI_TOP_K = 40
