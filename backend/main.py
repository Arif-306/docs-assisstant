from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import api

app = FastAPI(
    title="Docs Assistant API",
    description="Backend API for Docs Assistant project",
    version="1.0.0"
)

# ✅ Allow CORS (frontend aur backend ko connect karne ke liye zaroori)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend ka exact URL daal sakte ho yahan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route (server test karne ke liye)
@app.get("/")
async def root():
    return {"status": "ok", "message": "Backend is running!"}

# ✅ Import API routes
app.include_router(api.router, prefix="/api", tags=["API"])
