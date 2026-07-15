import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

filings_df = pd.read_csv("filings_data.csv", dtype={"company_number": str})
filings_df = filings_df.dropna(subset=["description"])

print("Loading embedding model (first run may take a minute)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="filings")

documents = []
metadatas = []
ids = []

for idx, row in filings_df.iterrows():
    text = f"{row['category']} filing on {row['date']}: {row['description']}"
    documents.append(text)
    metadatas.append({
        "company_number": row["company_number"],
        "category": row["category"],
        "date": str(row["date"]),
        "type": str(row["type"]),
    })
    ids.append(str(idx))

print(f"Embedding {len(documents)} filings...")
embeddings = model.encode(documents).tolist()

collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids,
)

print("Done. Total filings indexed:", collection.count())