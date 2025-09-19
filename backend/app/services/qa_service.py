from app.models.embeddings_store import VectorStore
from app.models.model_manager import ModelManager


vs = VectorStore()
mm = ModelManager()


def answer_question(question: str, top_k: int = 3):
hits = vs.query(question, top_k=top_k)
# join top hits into a single context (you can refine ordering)
context = "\n\n".join([h['text'] for h in hits])
resp = mm.answer(question, context)
return {
'answer': resp.get('answer'),
'score': float(resp.get('score', 0.0)),
'sources': hits
}