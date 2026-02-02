import os
from typing import List

from pymongo import MongoClient
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models import embedding_model, index
from config import (
    MONGODB_URI,
    DATA_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

import certifi

mongo_client = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = mongo_client["rag_db"]
collection = db["documents"]


def load_documents() -> List[str]:
    documents = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
                documents.append(f.read())
    return documents


def chunk_documents(docs: List[str]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.create_documents(docs)


def ingest_documents():
    docs = load_documents()
    chunks = chunk_documents(docs)

    vectors = []

    for chunk in chunks:
        embedding = embedding_model.encode(
            chunk.page_content,
            normalize_embeddings=True
        ).tolist()

        mongo_result = collection.insert_one({
            "content": chunk.page_content,
            "metadata": chunk.metadata
        })

        vectors.append({
            "id": str(mongo_result.inserted_id),
            "values": embedding,
            "metadata": {
                "text": chunk.page_content
            }
        })

    index.upsert(vectors=vectors)
    print(f"✅ Ingested {len(vectors)} chunks successfully.")


if __name__ == "__main__":
    ingest_documents()
