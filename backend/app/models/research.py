import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.core.database import Base

class ResearchDocument(Base):
    """Section 56 & 57 RAG / Knowledge System & Research Library"""
    __tablename__ = "research_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False) # PDF, DOCX, TXT, UN_RECORD
    title = Column(String(255), nullable=False)
    topic = Column(String(100), nullable=True)
    region = Column(String(50), nullable=True)
    country_focus = Column(String(10), nullable=True) # e.g. FRA, RUS, CHN
    summary = Column(Text, nullable=True)
    full_text = Column(Text, nullable=False)
    chunks_count = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, index=True)
    chunk_index = Column(Integer, default=0)
    content = Column(Text, nullable=False)
    keywords = Column(JSON, default=list)
