import pandas as pd
import chromadb

df = pd.read_csv("../data/filings_data.csv")
print("Total rows in CSV:", len(df))
print("Unique companies in CSV:", df["company_number"].nunique())
print("Is 01962348 in CSV company_number column?", "01962348" in df["company_number"].astype(str).values)

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="filings")
all_data = collection.get(limit=100000)
ingested_companies = set(m.get("company_number") for m in all_data["metadatas"])
print("Unique companies ingested into Chroma:", len(ingested_companies))