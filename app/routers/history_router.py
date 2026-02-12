from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.quiz_schema import QuizSummary
from app.services.quiz_service import QuizService


router = APIRouter(prefix="/quizzes", tags=["history"])


@router.get("", response_model=List[QuizSummary])
def list_quizzes(db: Session = Depends(get_db)):
    """Return a list of all previous quizzes."""
    service = QuizService(db)
    items = service.list_quizzes()
    return items

