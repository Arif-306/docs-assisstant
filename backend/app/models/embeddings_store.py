import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
def __init__(self, dim:int = 384, index_path: str = 'data/index/faiss.index', meta_path: str = 'data/index/meta.pkl'):
self.index_path = index_path
self.meta_path = meta_path
self.model = SentenceTransformer('all-MiniLM-L6-v2')
self.dim = dim
if os.path.exists(index_path) and os.path.exists(meta_path):
self.index = faiss.read_index(index_path)
with open(meta_path, 'rb') as f:
self.meta = pickle.load(f)
else:
# use inner product with normalized vectors
self.index = faiss.IndexFlatIP(dim)
self.meta = []


def add(self, texts: list, metas: list):
# texts: list of strings
embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
# normalize for IP
embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
self.index.add(embeddings.astype('float32'))
self.meta.extend(metas)
faiss.write_index(self.index, self.index_path)
with open(self.meta_path, 'wb') as f:
pickle.dump(self.meta, f)


def query(self, query_text: str, top_k: int = 5):
q_emb = self.model.encode([query_text], convert_to_numpy=True)
q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)
D, I = self.index.search(q_emb.astype('float32'), top_k)
results = []
for idx in I[0]:
if idx < len(self.meta):
results.append(self.meta[idx])
return results