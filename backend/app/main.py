from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routes.api import router as api_router


app = FastAPI(title="AlphaDoc Assistant")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


app.include_router(api_router, prefix="/api")


@app.get("/health")
def health():
return {"status":"ok"}