import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="filings")

all_data = collection.get(limit=100000)
matches = [m for m in all_data["metadatas"] if "1962348" in str(m.get("company_number", ""))]

print("Total documents in collection:", len(all_data["metadatas"]))
print("Matches containing '1962348':", len(matches))
for m in matches[:10]:
    print(m)