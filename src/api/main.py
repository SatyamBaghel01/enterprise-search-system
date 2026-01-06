from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from config.settings import settings
from datetime import datetime
import uvicorn

# print("SETTINGS LOADED FROM:", settings.__class__.__module__, settings.__class__.__file__)
print("Settings loaded:", settings)
app = FastAPI(
    title="Enterprise Search API",
    description="Intelligent multi-source enterprise search with AI",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {
        "message": "Enterprise Search API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)