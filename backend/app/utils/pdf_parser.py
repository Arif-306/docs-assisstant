import PyPDF2


def extract_text_from_pdf(path: str) -> str:
text_pages = []
with open(path, 'rb') as f:
reader = PyPDF2.PdfReader(f)
for page in reader.pages:
page_text = page.extract_text() or ""
text_pages.append(page_text)
return "\n".join(text_pages)