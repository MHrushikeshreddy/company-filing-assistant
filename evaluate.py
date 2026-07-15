import os
import re
import time
import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from google import genai

load_dotenv()
client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="filings")

eval_df = pd.read_csv("eval_questions_large.csv")
results = []


def generate_with_retry(model, prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            return client_ai.models.generate_content(model=model, contents=prompt)
        except Exception as e:
            wait = 10 * (attempt + 1)
            print(f"  Busy, retrying in {wait}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait)
    return None


for _, row in eval_df.iterrows():
    query = row["question"]
    expected = row["expected_answer_contains"].lower()

    company_match = re.search(r'\b\d{7,8}\b', query)
    where_filter = {"company_number": company_match.group()} if company_match else None

    n_results = 25 if where_filter else 10

   
    query_embedding = embed_model.encode([query]).tolist()
    retrieved = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        where=where_filter,
    )
    docs = retrieved["documents"][0]
    context = "\n".join(f"- {d}" for d in docs)

    prompt = f"""Answer using ONLY these filing records. If not found, say so.

Records:
{context}

Question: {query}
Answer:"""

    print(f"Asking: {query}")
    response = generate_with_retry("gemini-flash-lite-latest", prompt)

    if response is None:
        print("  FAILED after all retries, skipping.")
        results.append({
            "question": query,
            "expected_contains": expected,
            "ai_answer": "FAILED - server unavailable",
            "passed": False,
        })
        continue

    answer = response.text.lower()
    passed = expected in answer
    print(f"  Passed: {passed}")
    results.append({
        "question": query,
        "expected_contains": expected,
        "ai_answer": response.text,
        "passed": passed,
    })
    time.sleep(3)

results_df = pd.DataFrame(results)
results_df.to_csv("eval_results.csv", index=False)

accuracy = results_df["passed"].mean() * 100
print("\n" + results_df[["question", "passed"]].to_string(index=False))
print(f"\nAccuracy: {accuracy:.1f}% ({results_df['passed'].sum()}/{len(results_df)})")