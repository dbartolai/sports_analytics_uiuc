from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set! Check Railway Variables tab.")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)



print("Using DATABASE_URL:", DATABASE_URL[:50], "...")  # log prefix for sanity


class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables defined by your models"""
    from .auth.models import User
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all database tables - BE CAREFUL!"""
    Base.metadata.drop_all(bind=engine)
