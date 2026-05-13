import chromadb
from sentence_transformers.SentenceTransformer import SentenceTransformer

VECTORSTORE_DIR = "vectorstore"
COLLECTION_NAME = "documents"


def search_documents(
    query: str,
    n_results: int = 3,
    document_id: str | None = None
):
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=VECTORSTORE_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    query_embedding = embedding_model.encode(query).tolist()

    where_filter = None

    if document_id:
        where_filter = {"document_id": document_id}

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_filter,
        include=["documents", "metadatas", "distances"]
    )

    return results


if __name__ == "__main__":
    query = "What technologies are mentioned?"

    results = search_documents(query, n_results=2)

    print("Pergunta:", query)
    print("\nTrechos mais relevantes:")

    for doc in results["documents"][0]:
        print("\n---")
        print(doc)