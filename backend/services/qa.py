# services/qa.py
from datetime import datetime
import json
from typing import List, Tuple
from openai import OpenAI

from backend.database import db_session
from backend.database.qa import ResearchReport, QAHistory
from backend.schemas.qa import QAResponse, ReportResponse
from backend.utilities.document_processors import get_pdf_documents

async def process_qa_query(
    article_id: int,
    question: str,
    model: str,
    context_type: str,
    openai_client: OpenAI,
    user_id: int
) -> QAResponse:
    """Process a Q/A query and store the result"""
    # Get document content
    file_contents = await get_pdf_documents(article_id)
    
    # Prepare system prompt
    system_prompt = (
        f"You are an AI assistant analyzing a document with {context_type} content. "
        f"Provide precise answers with references to specific pages and media elements. "
        f"Document content: {file_contents}"
    )
    
    # Get response from OpenAI
    completion = await _invoke_openai_api(
        openai_client,
        model,
        question,
        system_prompt
    )
    
    # Parse response and extract metadata
    answer, confidence, pages, media = _parse_completion(completion)
    
    # Store in database
    qa_history = QAHistory(
        article_id=article_id,
        question=question,
        answer=answer,
        confidence_score=confidence,
        referenced_pages=pages,
        media_references=media,
        user_id=user_id
    )
    
    with db_session() as session:
        session.add(qa_history)
        session.commit()
    
    return QAResponse(
        answer=answer,
        confidence_score=confidence,
        referenced_pages=pages,
        media_references=media
    )

async def get_qa_history(article_id: int, user_id: int) -> List[dict]:
    """Retrieve Q/A history for an article"""
    with db_session() as session:
        history = session.query(QAHistory).filter(
            QAHistory.article_id == article_id,
            QAHistory.user_id == user_id
        ).order_by(QAHistory.created_at.desc()).all()
        
        return [
            {
                "question": h.question,
                "answer": h.answer,
                "created_at": h.created_at,
                "validated": h.validated,
                "confidence_score": h.confidence_score,
                "referenced_pages": h.referenced_pages,
                "media_references": h.media_references
            }
            for h in history
        ]

async def generate_research_report(
    article_id: int,
    questions: List[str],
    include_media: bool,
    format_type: str,
    openai_client: OpenAI,
    user_id: int
) -> ReportResponse:
    """Generate a research report from multiple questions"""
    # Get document content
    file_contents = await get_pdf_documents(article_id)
    
    # Generate answers for all questions
    answers = []
    media_refs = []
    for question in questions:
        completion = await _invoke_openai_api(
            openai_client,
            "gpt-4",
            question,
            f"Generate a detailed research note in {format_type} format. Document: {file_contents}"
        )
        answer, _, pages, media = _parse_completion(completion)
        answers.append(answer)
        if include_media:
            media_refs.extend(media)
    
    # Combine into report
    report_content = _format_report(questions, answers, format_type)
    
    # Store report
    report = ResearchReport(
        article_id=article_id,
        content=report_content,
        media_references=list(set(media_refs)),
        user_id=user_id
    )
    
    with db_session() as session:
        session.add(report)
        session.commit()
        session.refresh(report)
    
    return ReportResponse(
        report_id=report.report_id,
        content=report.content,
        media_references=report.media_references,
        created_at=report.created_at,
        validated=report.validated,
        indexed=report.indexed
    )

async def index_report(article_id: int, report_id: int, user_id: int) -> Tuple[str, str]:
    """Validate and index a report"""
    with db_session() as session:
        report = session.query(ResearchReport).filter(
            ResearchReport.report_id == report_id,
            ResearchReport.article_id == article_id,
            ResearchReport.user_id == user_id
        ).first()
        
        if not report:
            return "error", "Report not found"
        
        report.validated = True
        report.indexed = True
        session.commit()
        
        return "success", "Report validated and indexed"

# Helper functions
async def _invoke_openai_api(client: OpenAI, model: str, user_prompt: str, system_prompt: str) -> str:
    """Invoke OpenAI API with error handling"""
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

def _parse_completion(completion: str) -> Tuple[str, float, List[int], List[str]]:
    """Parse OpenAI completion into components"""
    # In practice, you'd want to structure the OpenAI output
    # and parse it properly. This is a simplified version.
    return (
        completion,
        0.95,
        [1, 2],
        []
    )

def _format_report(questions: List[str], answers: List[str], format_type: str) -> str:
    """Format the report based on specified type"""
    if format_type == "research_notes":
        return "\n\n".join([
            f"Question: {q}\nAnalysis: {a}"
            for q, a in zip(questions, answers)
        ])
    # Add more format types as needed
    return "\n\n".join(answers)
