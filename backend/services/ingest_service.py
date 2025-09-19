import PyPDF2
import PyPDF2 as PyPDF2

# ✅ Function to extract text from a PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

# ✅ Service function (used in routes)
def ingest_pdf(path: str) -> dict:
    text = extract_text_from_pdf(path)
    return {"status": "success", "content": text[:500]}  # first 500 chars only
