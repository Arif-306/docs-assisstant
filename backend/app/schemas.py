from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# -------------------------------
# Request Schemas
# -------------------------------
class QueryRequest(BaseModel):
    question: str = Field(..., example="What are the main conclusions of this PDF?")
    top_k: Optional[int] = Field(3, example=3)

class SummarizeRequest(BaseModel):
    text: str = Field(..., example="Enter text you want to summarize here.")

# -------------------------------
# Response Schemas
# -------------------------------
class SourceChunk(BaseModel):
    doc_id: str
    chunk_id: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    score: float
    sources: List[SourceChunk]

class UploadResponse(BaseModel):
    status: str
    doc_id: str
    chunks: int

class SummaryResponse(BaseModel):
    summary: str
