"""
Configuration settings for the chatbot.
All settings in one place = easy to change later!
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# DATABASE CONFIGURATION
# ============================================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "pizza_db")

# ============================================
# LLM (Language Model) CONFIGURATION
# ============================================

LLM_MODEL = "mistral"
EMBEDDING_MODEL = "mistral"

# ============================================
# VECTOR DATABASE CONFIGURATION
# ============================================

VECTOR_DB_PATH = "./vector_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ============================================
# LOGGING CONFIGURATION
# ============================================

DEBUG = True

# Simple test
if __name__ == "__main__":
    print("✅ Configuration loaded successfully!")
    print(f"Database: {DB_HOST}/{DB_NAME}")
    print(f"LLM Model: {LLM_MODEL}")