# models.py
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from langchain_groq import ChatGroq

from config import (
    EMBEDDING_MODEL_NAME,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    GROQ_API_KEY,
    LLM_MODEL_NAME,
)

print("🔄 Loading embedding model...")
embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME,
    device="cpu"
)

print("🔄 Connecting to Pinecone...")
pinecone = Pinecone(api_key=PINECONE_API_KEY)
index = pinecone.Index(PINECONE_INDEX_NAME)

print("🔄 Loading Groq LLM...")
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=LLM_MODEL_NAME,
    temperature=0
)

print("✅ Models loaded successfully")
