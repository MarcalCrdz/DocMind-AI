import os
import uuid

import chromadb
from sentence_transformers.SentenceTransformer import SentenceTransformer

from src.ingestion.load_documents import load_pdf_text
from src.ingestion.split_documents import split_text

VECTORSTORE_DIR = "vectorstore"
COLLECTION_NAME = "documents"


def index_pdf(file_path: str) -> dict:
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    text = load_pdf_text(file_path)
    chunks = split_text(text)

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=VECTORSTORE_DIR)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    document_id = str(uuid.uuid4())

    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()

        collection.add(
            ids=[f"{document_id}_chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{
                "source": file_path,
                "document_id": document_id,
                "chunk_id": i
            }]
        )

    return {
        "document_id": document_id,
        "file_path": file_path,
        "chunks_indexed": len(chunks)
    }