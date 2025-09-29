import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine
from .auth import routes as auth_routes

app = FastAPI(title="Sports Analytics API")

# Create database tables on startup

# Get environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

print(f" Environment: {ENVIRONMENT}")
print(f" Frontend URL: {FRONTEND_URL}")

# More permissive CORS configuration for debugging
origins = [
    "https://sports-analytics-uiuc.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "*"  # Temporarily allow all origins for debugging
]

print(f"🔒 CORS origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all origins
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Sports Analytics API", "environment": ENVIRONMENT}

@app.get("/health")
async def health():
    try:
        from .db import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "error", "message": str(e)}

@app.get("/cors-test")
async def cors_test():
    return {
        "message": "CORS test endpoint",
        "environment": ENVIRONMENT,
        "frontend_url": FRONTEND_URL,
        "origins": origins
    }
