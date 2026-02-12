from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.quiz_schema import GenerateQuizRequest, GenerateQuizResponse, QuizDetail
from app.services.quiz_service import QuizService


router = APIRouter(prefix="/generate-quiz", tags=["quiz"])


@router.post("", response_model=GenerateQuizResponse)
def generate_quiz(
    payload: GenerateQuizRequest,
    db: Session = Depends(get_db),
):
    """Generate a quiz from a Wikipedia article URL."""
    service = QuizService(db)
    try:
        result = service.generate_quiz(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    return result


@router.get("/{quiz_id}", response_model=QuizDetail)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
):
    """Fetch a single quiz by ID."""
    service = QuizService(db)
    result = service.get_quiz_by_id(quiz_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    return result

