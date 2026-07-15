import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

df = pd.read_csv("filings_data.csv")
df["company_number"] = df["company_number"].astype(str).str.zfill(8)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chroma_db")
client.delete_collection(name="filings")
collection = client.create_collection(name="filings")

documents = []
metadatas = []
ids = []

for idx, row in df.iterrows():
    doc_text = (
        f"Company {row['company_number']}: {row['category']} filing - "
        f"{row['description']} (type: {row['type']}, date: {row['date']})"
    )
    documents.append(doc_text)
    metadatas.append({
        "company_number": row["company_number"],
        "category": row["category"],
        "description": row["description"],
        "date": row["date"],
        "type": row["type"],
    })
    ids.append(f"filing_{idx}")

print(f"Encoding {len(documents)} documents...")
embeddings = embed_model.encode(documents, show_progress_bar=True).tolist()

collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids,
)

print(f"Ingested {collection.count()} documents into Chroma.")