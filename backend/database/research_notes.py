from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from datetime import datetime
from backend.database import Base

class ResearchNoteModel(Base):
    __tablename__ = "research_notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    validated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)