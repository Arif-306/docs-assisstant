# backend/models/embeddings_store.py

import os
import pickle
from typing import List, Optional

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    """
    Simple FAISS-backed vector store using SentenceTransformer embeddings.
    """

    def __init__(
        self,
        dim: int = 384,
        index_path: str = "data/index/faiss.index",
        meta_path: str = "data/index/meta.pkl",
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.dim = dim
        self.index_path = index_path
        self.meta_path = meta_path

        # load sentence-transformers model
        self.model = SentenceTransformer(model_name)

        # ensure index directory exists
        index_dir = os.path.dirname(self.index_path)
        if index_dir:
            os.makedirs(index_dir, exist_ok=True)

        # load index + meta if exist, otherwise create new
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.meta_path, "rb") as f:
                    self.meta = pickle.load(f)
            except Exception:
                # fallback to new index if loading fails
                self.index = faiss.IndexFlatIP(self.dim)
                self.meta = []
        else:
            # use inner product on normalized vectors for similarity
            self.index = faiss.IndexFlatIP(self.dim)
            self.meta = []

    def add(self, texts: List[str], metas: Optional[List[dict]] = None):
        """
        Add texts to the index. `metas` should be a list of metadata objects
        (e.g. dicts containing 'text', 'source', ...). If metas is None,
        we'll store the original text as the meta.
        """
        if metas is None:
            metas = [{"text": t} for t in texts]

        # compute embeddings as numpy array
        embeddings = self.model.encode(
            texts, convert_to_numpy=True, show_progress_bar=False
        )

        # normalize embeddings to unit vectors to use inner product as cosine
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        # avoid division by zero
        norms[norms == 0] = 1.0
        embeddings = embeddings / norms

        # ensure float32
        embeddings = embeddings.astype("float32")

        # add to index and meta
        self.index.add(embeddings)
        self.meta.extend(metas)

        # persist
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.meta, f)

    def query(self, query_text: str, top_k: int = 5) -> List[dict]:
        """
        Query the index with a text. Returns list of dicts:
        [{'text': ..., 'score': float, 'meta': <meta_object>}, ...]
        """
        if self.index.ntotal == 0:
            return []

        # compute query embedding and normalize
        q_emb = self.model.encode([query_text], convert_to_numpy=True)
        q_norm = np.linalg.norm(q_emb, axis=1, keepdims=True)
        if q_norm[0][0] == 0:
            q_norm[0][0] = 1.0
        q_emb = (q_emb / q_norm).astype("float32")

        # search
        D, I = self.index.search(q_emb, top_k)

        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < len(self.meta) and idx != -1:
                meta_obj = self.meta[idx]
                # try to extract stored text; fallback to meta itself
                text = meta_obj.get("text") if isinstance(meta_obj, dict) else str(meta_obj)
                results.append({"text": text, "score": float(dist), "meta": meta_obj})
        return results

    def save(self):
        """Explicitly save index and meta to disk."""
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.meta, f)

    def load(self):
        """Load index and meta from disk (if available)."""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        if os.path.exists(self.meta_path):
            with open(self.meta_path, "rb") as f:
                self.meta = pickle.load(f)
