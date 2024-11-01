# views/qa.py
from fastapi import APIRouter, status, HTTPException, Depends
from openai import OpenAI
from typing import List

from backend.schemas.qa import (
    QARequest,
    QAResponse,
    ChatHistoryResponse,
    ReportGenerationRequest,
    ReportResponse,
    IndexReportResponse
)
from backend.services.qa import (
    process_qa_query,
    get_qa_history,
    generate_research_report,
    index_report
)
from backend.services.auth_bearer import get_current_user_id
from backend.services.qa import _invoke_openai_api

qa_router = APIRouter(prefix="/chat", tags=["qa-interface"])

@qa_router.post(
    "/{article_id}/qa",
    response_model=QAResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_404_NOT_FOUND: {"description": "Article not found"}
    }
)
async def question_answer(
    article_id: int,
    request: QARequest,
    openai_client: OpenAI = Depends(_invoke_openai_api),
    user_id: int = Depends(get_current_user_id)
) -> QAResponse:
    """
    Process a Q/A query for a specific article using multi-modal RAG
    """
    try:
        return await process_qa_query(
            article_id,
            request.question,
            request.model,
            request.context_type,
            openai_client,
            user_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@qa_router.get(
    "/{article_id}/history",
    response_model=List[ChatHistoryResponse]
)
async def get_history(
    article_id: int,
    user_id: int = Depends(get_current_user_id)
) -> List[ChatHistoryResponse]:
    """
    Retrieve Q/A history for a specific article
    """
    try:
        history = await get_qa_history(article_id, user_id)
        return [ChatHistoryResponse(**h) for h in history]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@qa_router.post(
    "/{article_id}/generate-report",
    response_model=ReportResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_404_NOT_FOUND: {"description": "Article not found"}
    }
)
async def create_report(
    article_id: int,
    request: ReportGenerationRequest,
    openai_client: OpenAI = Depends(_invoke_openai_api),
    user_id: int = Depends(get_current_user_id)
) -> ReportResponse:
    """
    Generate a comprehensive research report for an article
    """
    try:
        return await generate_research_report(
            article_id,
            request.questions,
            request.include_media,
            request.format_type,
            openai_client,
            user_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@qa_router.post(
    "/{article_id}/{report_id}/index",
    response_model=IndexReportResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_404_NOT_FOUND: {"description": "Report not found"}
    }
)
async def validate_and_index_report(
    article_id: int,
    report_id: int,
    user_id: int = Depends(get_current_user_id)
) -> IndexReportResponse:
    """
    Validate and index a generated report
    """
    try:
        status, message = await index_report(article_id, report_id, user_id)
        return IndexReportResponse(status=status, message=message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
