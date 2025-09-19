import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, '..', '..', 'data', 'uploads')
INDEX_DIR = os.path.join(BASE_DIR, '..', '..', 'data', 'index')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)