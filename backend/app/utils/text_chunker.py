import re


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 200):
# simple word-based chunker
words = text.split()
chunks = []
start = 0
while start < len(words):
end = min(start + chunk_size, len(words))
chunk = " ".join(words[start:end])
chunks.append(chunk)
start = end - overlap
return chunks