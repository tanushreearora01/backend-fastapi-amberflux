from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
 
URL_Database = os.getenv("DATABASE_URL", "postgresql://admin:YKmcce3Pe9H4mgmBWOvzMPYqYBgjeNnq@dpg-d30adkvdiees73eshj60-a.oregon-postgres.render.com/document_library")
engine = create_engine(URL_Database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()