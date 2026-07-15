import re
import os
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv

load_dotenv()
client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="filings")

print("Company Filing Assistant — type 'quit' to exit\n")

while True:
    query = input("Ask a question about a company: ").strip()
    if query.lower() in ("quit", "exit"):
        break

    company_match = re.search(r'\b(?=[A-Z0-9]{7,8}\b)[A-Z]{0,2}\d{6,8}\b', query.upper())
    where_filter = {"company_number": company_match.group().zfill(8)} if company_match else None
    n_results = 25 if where_filter else 10

    print(f"[DEBUG] Filter: {where_filter}")

    query_embedding = embed_model.encode([query]).tolist()
    retrieved = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        where=where_filter,
    )
    docs = retrieved["documents"][0]
    context = "\n".join(f"- {d}" for d in docs)

    prompt = f"""Answer using ONLY these filing records. If the specific information isn't present, clearly state that (e.g. "No, there is no dissolution record" rather than just "Not found").

Records:
{context}

Question: {query}
Answer:"""

    response = client_ai.models.generate_content(model="gemini-flash-lite-latest", contents=prompt)
    print(f"\n{response.text}\n")