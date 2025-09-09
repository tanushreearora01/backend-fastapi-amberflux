import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:YKmcce3Pe9H4mgmBWOvzMPYqYBgjeNnq@dpg-d30adkvdiees73eshj60-a.oregon-postgres.render.com/document_library"
)

# Convert postgres:// to postgresql:// for psycopg2 compatibility
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Add SSL mode for production deployments
if "sslmode=" not in DATABASE_URL and ("render.com" in DATABASE_URL or "herokuapp.com" in DATABASE_URL):
    sep = "&" if "?" in DATABASE_URL else "?"
    DATABASE_URL = f"{DATABASE_URL}{sep}sslmode=require"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()