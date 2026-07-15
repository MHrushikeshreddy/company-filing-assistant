import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="filings")

while True:
    query = input("\nAsk a question about the filings (or type 'exit'): ")
    if query.lower() == "exit":
        break

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5,
    )

    print("\nTop matching filings:")
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"- [{meta['company_number']}] {doc}")
    