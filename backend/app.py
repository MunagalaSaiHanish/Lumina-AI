from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

app = FastAPI(
    title="Lumixa API",
    description="Production Backend for Lumixa AI",
    version="1.0.0"
)

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Lumixa API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "Lumixa",
        "version": "1.0.0"
    }