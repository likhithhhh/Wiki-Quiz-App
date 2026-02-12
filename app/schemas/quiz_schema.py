from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, HttpUrl


class MCQOption(BaseModel):
    text: str


class MCQQuestion(BaseModel):
    question: str
    options: List[MCQOption]
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: Optional[str] = None


class QuizData(BaseModel):
    questions: List[MCQQuestion]


class GenerateQuizRequest(BaseModel):
    url: HttpUrl


class GenerateQuizResponse(BaseModel):
    article: Dict[str, Any]
    quiz: QuizData
    related_topics: List[str]


class QuizSummary(BaseModel):
    id: int
    article_id: int
    article_title: str
    article_url: str
    created_at: datetime


class QuizDetail(BaseModel):
    id: int
    article: Dict[str, Any]
    quiz: QuizData
    related_topics: List[str]

    class Config:
        from_attributes = True

