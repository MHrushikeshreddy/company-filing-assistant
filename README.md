# Company Filing Assistant (RAG-based)

A Retrieval-Augmented Generation (RAG) assistant that answers natural language questions about UK company filings, built with a local vector index and an LLM-backed query pipeline.

## Overview

This project lets users ask plain-English questions about company filings data (e.g. "What was Company X's latest filing type?") and get grounded, accurate answers pulled directly from the underlying dataset rather than relying on LLM hallucination.

**Key results:** Achieved 100% accuracy on a held-out evaluation set of test questions (see `eval_results.csv`).

## Features

- Fetches and ingests UK company and filing data (`fetch_companies.py`, `fetch_filings.py`)
- Builds a searchable vector index over filings (`build_index.py`, `ingest.py`)
- Answers questions via a RAG pipeline combining retrieval + LLM generation (`ask_ai.py`, `search_filings.py`)
- Two interfaces: command-line (`query_cli.py`) and a Streamlit web app (`app.py`)
- Built-in evaluation harness to measure answer accuracy (`evaluate.py`, `generate_eval_set.py`)

## Tech Stack

- Python
- Vector embeddings + similarity search
- LLM API for answer generation
- Streamlit (web UI)
- Pandas (data handling)

## Project Structure

```
company-filing-assistant/
├── app.py                  # Streamlit web interface
├── query_cli.py             # Command-line query interface
├── ingest.py                 # Ingests and indexes filing data
├── build_index.py            # Builds the vector index
├── ask_ai.py                  # Core RAG query logic
├── search_filings.py         # Retrieval logic
├── fetch_companies.py        # Fetches company metadata
├── fetch_filings.py           # Fetches filing documents
├── evaluate.py                # Runs evaluation against eval_questions.csv
├── generate_eval_set.py       # Generates evaluation question sets
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. Clone the repository
   ```
   git clone https://github.com/MHrushikeshreddy/company-filing-assistant.git
   cd company-filing-assistant
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```
   cp .env.example .env
   # Add your API key(s) to .env
   ```

5. Build the index
   ```
   python ingest.py
   ```

## Usage

**Command line:**
```
python query_cli.py
```

**Web app:**
```
streamlit run app.py
```

**Example:**
> Q: "What type of filing did [Company] submit most recently?"
> A: The assistant retrieves relevant filing records and generates a grounded answer with source context.

## Evaluation

Run the evaluation suite to reproduce accuracy results:
```
python evaluate.py
```
Results are saved to `eval_results.csv`. Current benchmark: 100% accuracy on `eval_questions.csv`.

## Roadmap

- [ ] Connect to live Companies House API instead of static CSV snapshot
- [ ] Add dropdown/autocomplete for company name search in the UI
- [ ] Display raw retrieved records alongside generated answers
- [ ] Deploy the Streamlit app publicly

## License

This project is licensed under the MIT License. See `LICENSE` for details.
