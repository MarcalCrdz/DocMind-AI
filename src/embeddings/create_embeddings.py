import os

import chromadb
from sentence_transformers.SentenceTransformer import SentenceTransformer

from src.ingestion.load_documents import load_pdf_text
from src.ingestion.split_documents import split_text

PDF_PATH = "data/raw/Curriculo_pedro_v2.pdf"
VECTORSTORE_DIR= "vectorstore"
COLLECTION_NAME = "documents"

def main():

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    print("Carregando PDF...")
    text = load_pdf_text(PDF_PATH)

    print("Dividindo texto em chunks...")
    chunks = split_text(text)

    print(f"Total de chunks: {len(chunks)}")

    print ("Carregando modelo de embeddings...")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Criando banco vetorial...")
    client = chromadb.PersistentClient(path=VECTORSTORE_DIR)

    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    print("Gerando embeddings e salvando no ChromaDB...")

    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()

        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"source": PDF_PATH, "chunk_id": i}]
        )

        print("Embeddings salvoss com sucesso!")

if __name__ == "__main__":
    main()