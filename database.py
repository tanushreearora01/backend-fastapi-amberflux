from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
 
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:YKmcce3Pe9H4mgmBWOvzMPYqYBgjeNnq@dpg-d30adkvdiees73eshj60-a.oregon-postgres.render.com/document_library")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()