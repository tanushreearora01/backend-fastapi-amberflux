from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
URL_Database = "postgresql://postgres:12345@localhost:5432/document_library"

engine = create_engine(URL_Database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()