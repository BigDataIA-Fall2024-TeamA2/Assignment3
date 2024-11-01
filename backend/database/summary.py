
from sqlalchemy import Column, String, Integer, DateTime, Computed, Sequence
from backend.database import Base

class ArticleModel(Base):
    __tablename__ = "articles"


    a_id = Column(
        'a_id',
        String,
        nullable=False
    )
    generated_summary = Column(String)
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