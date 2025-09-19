from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from backend.services.ingest_service import ingest_pdf
from backend.services.qa_service import answer_question
from app.models.model_manager import ModelManager
from app.core import config

router = APIRouter()
mm = ModelManager()  # for summarization or extra features

# -------------------------------
# PDF Upload Endpoint
# -------------------------------
@router.post('/upload')
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file.
    - Only accepts PDF.
    - Saves in data/uploads/
    - Calls ingest service to chunk & create embeddings.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Only PDF files are allowed.')

    file_path = os.path.join(config.UPLOAD_DIR, file.filename)
    content = await file.read()
    with open(file_path, 'wb') as f:
        f.write(content)

    doc_id = file.filename.replace('.pdf', '')
    num_chunks = ingest_pdf(file_path, doc_id)

    return JSONResponse({
        "status": "ingested",
        "doc_id": doc_id,
        "chunks": num_chunks
    })

# -------------------------------
# Question Answering Endpoint
# -------------------------------
@router.post('/query')
async def query(payload: dict):
    """
    Send a question about uploaded PDFs.
    - payload example: { "question": "...", "top_k": 3 }
    """
    question = payload.get("question")
    top_k = payload.get("top_k", 3)

    if not question:
        raise HTTPException(status_code=400, detail="Question is required.")

    try:
        res = answer_question(question, top_k=top_k)
        return JSONResponse(res)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# -------------------------------
# Summarization Endpoint
# -------------------------------
@router.post('/summarize')
async def summarize(payload: dict):
    """
    Summarize a document or text.
    - payload example: { "text": "..." }
    """
    text = payload.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required for summarization.")

    try:
        summary = mm.summarize(text)
        return JSONResponse({"summary": summary})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# -------------------------------
# Health Check Endpoint
# -------------------------------
@router.get('/health')
async def health_check():
    return {"status": "ok", "message": "AlphaDoc Assistant is running"}



from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"msg": "Hello from API"}

