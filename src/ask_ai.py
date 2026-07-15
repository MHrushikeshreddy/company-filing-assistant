import os
import time
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from google import genai

load_dotenv()
client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="../chroma_db")
collection = client.get_or_create_collection(name="filings")


def generate_with_retry(model, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client_ai.models.generate_content(model=model, contents=prompt)
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Model busy, retrying in 5 seconds... (attempt {attempt + 1})")
                time.sleep(5)
            else:
                raise e


while True:
    query = input("\nAsk a question about the filings (or type 'exit'): ")
    if query.lower() == "exit":
        break

    query_embedding = embed_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=5)

    retrieved_docs = results["documents"][0]
    context = "\n".join(f"- {doc}" for doc in retrieved_docs)

    prompt = f"""You are a UK company filings assistant. Answer the question using ONLY the filing records below. If the records don't contain the answer, say so clearly. Cite the specific filing details you used.

Filing records:
{context}

Question: {query}

Answer:"""

    response = generate_with_retry("gemini-3.5-flash", prompt)

    print("\n--- AI Answer ---")
    print(response.text)
    print("\n--- Sources used ---")
    for doc in retrieved_docs:
        print(f"- {doc}")