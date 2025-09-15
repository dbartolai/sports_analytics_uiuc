import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import dev

app = FastAPI(title="Sports Analytics API")

# Get environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Configure CORS
if ENVIRONMENT == "development":
    origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
    ]
else:
    origins = [
        "https://sports-analytics-uiuc.vercel.app",  # Your actual Vercel URL
        FRONTEND_URL,
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dev.router, prefix="/devs", tags=["devs"])

@app.get("/")
async def root():
    return {"message": "Sports Analytics API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
