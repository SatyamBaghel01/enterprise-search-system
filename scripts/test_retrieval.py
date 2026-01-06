from src.ingestion.embedder import Embedder
from src.storage.vector_store import VectorStore

def run_retrieval_test():
    print("Starting retrieval test...")

    embedder = Embedder()
    vector_store = VectorStore()

    query = "What is this document about?"
    print(f"\nQuery: {query}")

    query_embedding = embedder.embed_text(query)

    results = vector_store.search(
        query_embedding=query_embedding,
        n_results=5
    )

    print("\nResults:")
    for idx, r in enumerate(results, start=1):
        print(f"\nResult {idx}")
        print("ID:", r["id"])
        print("Score:", round(r["score"], 4))
        print("Content:", r["content"][:200], "...")
        print("Metadata:", r["metadata"])

if __name__ == "__main__":
    run_retrieval_test()
