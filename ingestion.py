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
from pypdf import PdfReader
from docx import Document


mongo_client = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = mongo_client["rag_db"]
collection = db["documents"]


# -------- FILE READERS -------- #

def read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)


def read_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


# -------- LOAD ALL DOCUMENTS -------- #

def load_documents() -> List[str]:
    documents = []

    for file in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file)
        ext = file.lower().split(".")[-1]

        try:
            if ext == "txt":
                documents.append(read_txt(file_path))

            elif ext == "pdf":
                documents.append(read_pdf(file_path))

            elif ext in ["docx", "doc"]:
                documents.append(read_docx(file_path))

        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")

    return documents


def chunk_documents(docs: List[str]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.create_documents(docs)


# -------- INGEST -------- #

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
