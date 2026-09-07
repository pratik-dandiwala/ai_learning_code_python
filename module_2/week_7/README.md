# Module 2 · Week 1 — Document Ingestion & Chunking

The first stage of "The Daily Planet AI Desk" RAG pipeline: load the newsroom
archive, extract clean text + metadata, and split it into embedding-ready chunks.

## What you build
- `rag/ingest.py` — loaders that turn messy files (markdown, HTML) into clean `Document`s with metadata.
- `rag/chunk.py` — token-aware chunking (`RecursiveCharacterTextSplitter`) that carries metadata onto each chunk.
- `explore.py` — a scratch file to *see* chunking behavior before it's wrapped into the pipeline: naive
  fixed-size cuts (which split mid-word) vs. recursive splitting (which respects paragraph/sentence
  boundaries) vs. overlap (why chunk seams repeat a few words into the next chunk). Not part of the
  final pipeline — run it to build intuition, then move on.
- `build_chunks.py` — the pipeline: ingest `data/` → chunk → save `chunks.jsonl`.

## Setup
```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python explore.py         # optional, but worth running first - see chunking strategies side by side
python build_chunks.py
```
Produces `chunks.jsonl` — the input to Week 2 (embeddings & vector search).

## Note
Week 1 does **not** call any LLM, so no API key is required. The `.env.example`
is here only to keep the project consistent for next week.

## The archive (`data/`)
A small, teaching-sized sample of newsroom content — clean markdown articles plus
one deliberately messy HTML wire story — so you can see ingestion and chunking on
realistic, mixed-format data.
