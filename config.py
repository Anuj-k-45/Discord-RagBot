import os
from dotenv import load_dotenv

load_dotenv()

# ===============================
# API KEYS
# ===============================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
BOT_TOKEN = os.getenv("TOKEN")

# ===============================
# MODEL CONFIG
# ===============================
# Local embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Embedding dimension (IMPORTANT)
EMBEDDING_DIMENSION = 384

# Groq chat model
LLM_MODEL_NAME = "llama-3.1-8b-instant"

# Pinecone index
PINECONE_INDEX_NAME = "rag-bot-v2"

# ===============================
# RAG SETTINGS
# ===============================
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
DATA_PATH = "data"
ENABLE_CHAT_HISTORY = False


# ===============================
# SAFETY CHECKS
# ===============================
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in environment variables")

if not PINECONE_API_KEY:
    raise ValueError("❌ PINECONE_API_KEY not found in environment variables")

if not MONGODB_URI:
    raise ValueError("❌ MONGODB_URI not found in environment variables")
