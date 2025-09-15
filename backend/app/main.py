import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import dev
from .db import engine
from .models import dev as dev_models

app = FastAPI(title="Sports Analytics API")

# Create database tables on startup
dev_models.Base.metadata.create_all(bind=engine)

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
    try:
        from .db import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "error", "message": str(e)}
