# articles/api.py
from fastapi import APIRouter, status, HTTPException
from typing import List
from backend.schemas.articles import (
    # ArticleCreate,
    ArticleResponse,
    ArticleSummaryRequest,
    ArticleSummaryResponse
)
from backend.services.articles import (
    # _create_article,
    _get_article,
    _get_all_articles,
    _generate_summary
)

articles_router = APIRouter(prefix="/articles", tags=["articles"])

# @articles_router.post(
#     "/",
#     response_model=ArticleResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_article(article: ArticleCreate) -> ArticleResponse:
#     if created_article := await _create_article(article=article):
#         return created_article
#     raise HTTPException(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         detail="Failed to create article"
#     )

@articles_router.get(
    "/",
    response_model=List[ArticleResponse],
)
async def get_all_articles() -> List[ArticleResponse]:
    articles = await _get_all_articles()
    return articles

@articles_router.get(
    "/{article_id}",
    response_model=ArticleResponse,
    responses={status.HTTP_404_NOT_FOUND: {"model": None}},
)
async def get_article(article_id: int) -> ArticleResponse:
    if article := await _get_article(article_id=article_id):
        return article
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Article with id {article_id} not found"
    )

@articles_router.post(
    "/generate-summary/{article_id}",
    response_model=ArticleSummaryResponse,
    responses={status.HTTP_404_NOT_FOUND: {"model": None}},
)
async def generate_summary(article_id: int) -> ArticleSummaryResponse:
    article = await _get_article(article_id=article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id {article_id} not found"
        )

    summary = await _generate_summary(article_id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate summary"
        )

    return ArticleSummaryResponse(
        article_id=article_id,
        title=article.title,
        summary=summary
    )
