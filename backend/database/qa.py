# database/models/qa.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship

from backend.database import Base

class ResearchReport(Base):
    __tablename__ = 'research_reports'
    
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer)
    content = Column(String)
    media_references = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    validated = Column(Boolean, default=False)
    indexed = Column(Boolean, default=False)
    user_id = Column(Integer)

    # # Relationships
    # article = relationship("Article", back_populates="reports")
    # user = relationship("User", back_populates="reports")

class QAHistory(Base):
    __tablename__ = 'qa_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer)
    question = Column(String)
    answer = Column(String)
    confidence_score = Column(Integer)
    referenced_pages = Column(JSON)
    media_references = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    validated = Column(Boolean, default=False)
    user_id = Column(Integer)

    # # Relationships
    # article = relationship("Article", back_populates="qa_history")
    # user = relationship("User", back_populates="qa_history")