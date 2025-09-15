from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set! Check Railway Variables tab.")

print("Using DATABASE_URL:", DATABASE_URL[:50], "...")  # log prefix for sanity


class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
