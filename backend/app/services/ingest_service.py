from app.utils.pdf_parser import extract_text_from_pdf
from app.utils.text_chunker import chunk_text
from app.models.embeddings_store import VectorStore


vs = VectorStore()


def ingest_pdf(path: str, doc_id: str):
text = extract_text_from_pdf(path)
chunks = chunk_text(text)
metas = []
texts = []
for i, ch in enumerate(chunks):
meta = {
'doc_id': doc_id,
'chunk_id': f"{doc_id}_{i}",
'text': ch
}
metas.append(meta)
texts.append(ch)
vs.add(texts, metas)
return len(chunks)