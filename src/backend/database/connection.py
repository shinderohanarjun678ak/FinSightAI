from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

# Read database credentials from environment variables

DB_USER = os.getenv("DB_USER","root")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD",""))
DB_HOST = os.getenv("DB_HOST","localhost")
DB_PORT = os.getenv("DB_PORT","3306")
DB_NAME = os.getenv("DB_NAME","finsight")


# Create the SQLAlchemy database URL

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create database engine

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Create database sessions

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Base class for SQLAlchemy models

Base = declarative_base()

# Provide a database session to API endpoints

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()