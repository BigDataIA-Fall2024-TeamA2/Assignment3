# articles/models.py
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Computed, Sequence
from backend.database import Base

class ArticleModel(Base):
    __tablename__ = "articles"

    article_id = Column(
        'article_id',
        Integer,
        Sequence('article_id_seq', schema='public'),
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    title = Column(String(500), nullable=False)
    description = Column(String(1000), nullable=False)
    publication_date = Column(DateTime, nullable=False)
    authors = Column(String(500), nullable=False)
    pdf_url = Column(String(500), nullable=False)
    image_url = Column(String(500), nullable=False)
    created_at = Column(
        DateTime,
        Computed("CURRENT_TIMESTAMP()"),
        nullable=False
    )
    updated_at = Column(
        DateTime,
        Computed("CURRENT_TIMESTAMP()"),
        nullable=False
    )

    __table_args__ = {'schema': 'public'}