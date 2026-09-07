"""Scratch file to SEE chunking behavior before we wrap it into the pipeline.

Run it:  python explore.py
This file is just for learning - the real chunking logic lives in rag/chunk.py.
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.ingest import ingest_folder
from rag.chunk import count_tokens, naive_chunk

docs = ingest_folder("data")
arena = [d for d in docs if d.metadata["source"] == "arena-budget-approved.md"][0]
print("Article tokens:", count_tokens(arena.text))

# 1) NAIVE fixed-size: blind cut every 300 characters
print("\n--- naive fixed-size (300 chars) ---")
pieces = naive_chunk(arena.text, size=300)
print("end of chunk 0 :", repr(pieces[0][-40:]))
print("start of chunk 1:", repr(pieces[1][:40]))

# 2) RECURSIVE: split on natural boundaries (paragraph -> sentence -> word)
print("\n--- recursive (120 tokens) ---")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=120,
    chunk_overlap=20,
    length_function=count_tokens,
    separators=["\n\n", "\n", ". ", " ", ""],
)
for i, piece in enumerate(splitter.split_text(arena.text)):
    print(f"chunk {i} ({count_tokens(piece)} tok) ends: ...{piece[-45:]!r}")

# 3) OVERLAP: the seam repeats a few words into the next chunk
print("\n--- overlap (word-level, size 25 / overlap 10) ---")
sentence = arena.text.split("\n\n")[0]
overlapper = RecursiveCharacterTextSplitter(
    chunk_size=25,
    chunk_overlap=10,
    length_function=count_tokens,
    separators=[" ", ""],
)
op = overlapper.split_text(sentence)
print("chunk 0 ends :", repr(op[0][-45:]))
print("chunk 1 start:", repr(op[1][:45]))
