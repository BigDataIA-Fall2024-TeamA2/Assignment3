# articles/schemas.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ArticleBase(BaseModel):
    title: str
    description: str
    publication_date: datetime
    authors: str
    pdf_url: str
    image_url: str

class ArticleCreate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    article_id: int
    created_at: datetime
    updated_at: datetime

class ArticleSummaryRequest(BaseModel):
    article_id: int

class ArticleSummaryResponse(BaseModel):
    article_id: int
    title: str
    summary: str
