import re
import os
import streamlit as st
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def load_resources():
    client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="filings")
    companies_df = pd.read_csv("companies_data.csv")
    companies_df["company_number"] = companies_df["company_number"].astype(str)
    return client_ai, embed_model, collection, companies_df

client_ai, embed_model, collection, companies_df = load_resources()

st.set_page_config(page_title="Company Filing Assistant", page_icon="📄")
st.title("📄 Company Filing Assistant")
st.caption("Ask questions about UK company filings by company number or name.")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask a question about a company:", placeholder="e.g. Was TPLC LIMITED dissolved?")

def resolve_company_number(query):
    match = re.search(r'\b(?=[A-Z0-9]{7,8}\b)[A-Z]{0,2}\d{6,8}\b', query.upper())
    if match:
        return match.group().zfill(8)

    for _, row in companies_df.iterrows():
        if row["company_name"].lower() in query.lower():
            return row["company_number"]
    return None

if st.button("Ask") and query.strip():
    company_number = resolve_company_number(query)
    where_filter = {"company_number": company_number} if company_number else None
    n_results = 25 if where_filter else 10

    status_note = ""
    if company_number:
        match_row = companies_df[companies_df["company_number"] == company_number]
        if not match_row.empty:
            status = match_row.iloc[0]["company_status"]
            name = match_row.iloc[0]["company_name"]
            status_note = f"Official status for {name} ({company_number}): {status}."

    with st.spinner("Searching filings..."):
        query_embedding = embed_model.encode([query]).tolist()
        retrieved = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            where=where_filter,
        )
        docs = retrieved["documents"][0]
        context = "\n".join(f"- {d}" for d in docs)

        prompt = f"""Answer using ONLY these filing records and the official status note below. Be direct: if the official status confirms the company is dissolved or active, use that fact explicitly in your answer.

Official status: {status_note if status_note else "Not available"}

Records:
{context}

Question: {query}
Answer:"""

        response = client_ai.models.generate_content(model="gemini-flash-lite-latest", contents=prompt)
        answer = response.text

    st.session_state.history.insert(0, {
        "question": query,
        "answer": answer,
        "filter": where_filter,
        "status_note": status_note,
    })

for item in st.session_state.history:
    st.markdown(f"**Q: {item['question']}**")
    if item["filter"]:
        st.caption(f"Filtered to company: {item['filter']['company_number']}")
    if item["status_note"]:
        st.caption(item["status_note"])
    st.write(item["answer"])
    st.divider()