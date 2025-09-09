import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    page_count = Column(Integer, nullable=True)
    status = Column(String, nullable=False, default="processing")
    created_at = Column(DateTime, default=datetime.utcnow)

    pages = relationship(
        "DocumentPage",
        back_populates="document",
        cascade="all, delete-orphan",
    )

class DocumentPage(Base):
    __tablename__ = "document_pages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    text = Column(Text)
    chunk_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="pages")