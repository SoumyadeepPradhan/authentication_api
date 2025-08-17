from typing import Generator
from sqlalchemy import create_engine
from core.config import get_settings
from sqlalchemy.orm import sessionmaker, declarative_base

settings=get_settings()
engine = create_engine(
    settings.DB_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0
)
SessionLocal=sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base=declarative_base()

def get_db()->Generator:
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
