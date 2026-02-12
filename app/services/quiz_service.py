from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.article_model import Article
from app.models.quiz_model import Quiz
from app.schemas.article_schema import ArticleCreate, ArticleInDB, ScrapedArticleContent
from app.schemas.quiz_schema import GenerateQuizRequest, QuizData
from app.services.entity_extractor import extract_entities
from app.services.llm_service import generate_quiz_and_topics
from app.services.scraper_service import InvalidWikipediaURLError, scrape_wikipedia_article


class QuizService:
    """High-level orchestration for scraping, generating, and persisting quizzes."""

    def __init__(self, db: Session) -> None:
        self.db = db

    # ---------------------------
    # Core workflow
    # ---------------------------

    def generate_quiz(self, payload: GenerateQuizRequest) -> Dict[str, Any]:
        """Generate or fetch a quiz for the given article URL."""
        # Cache: if we already have this URL, just return its latest quiz
        existing_article = self._get_article_by_url(str(payload.url))
        if existing_article:
            latest_quiz = (
                self.db.execute(
                    select(Quiz)
                    .where(Quiz.article_id == existing_article.id)
                    .order_by(Quiz.id.desc())
                )
                .scalars()
                .first()
            )
            if latest_quiz:
                return self._build_quiz_response(existing_article, latest_quiz)

        # Scrape article
        try:
            scraped: ScrapedArticleContent = scrape_wikipedia_article(str(payload.url))
        except InvalidWikipediaURLError as e:
            raise ValueError(str(e)) from e

        # Enrich with entities
        scraped.entities = extract_entities(scraped.text)

        # Call LLM for quiz and topics
        llm_result = generate_quiz_and_topics(scraped)
        quiz: QuizData = llm_result["quiz"]
        related_topics: List[str] = llm_result["related_topics"]

        # Persist article (or reuse existing) and quiz
        article_model = existing_article or self._create_article(scraped)
        quiz_model = self._create_quiz(article_model.id, quiz, related_topics)

        return self._build_quiz_response(article_model, quiz_model)

    # ---------------------------
    # Persistence helpers
    # ---------------------------

    def _get_article_by_url(self, url: str) -> Optional[Article]:
        stmt = select(Article).where(Article.url == url)
        return self.db.execute(stmt).scalars().first()

    def _create_article(self, scraped: ScrapedArticleContent) -> Article:
        article_in = ArticleCreate(
            url=scraped.url,
            title=scraped.title,
            summary=scraped.summary,
            sections={"sections": scraped.sections},
            entities=scraped.entities.model_dump(),
            raw_html=scraped.raw_html,
        )
        article = Article(
            url=str(article_in.url),
            title=article_in.title,
            summary=article_in.summary,
            sections=article_in.sections,
            entities=article_in.entities,
            raw_html=article_in.raw_html,
        )
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

    def _create_quiz(self, article_id: int, quiz: QuizData, related_topics: List[str]) -> Quiz:
        quiz_model = Quiz(
            article_id=article_id,
            quiz_data=quiz.model_dump(),
            related_topics=related_topics,
        )
        self.db.add(quiz_model)
        self.db.commit()
        self.db.refresh(quiz_model)
        return quiz_model

    # ---------------------------
    # Response builders
    # ---------------------------

    def _build_quiz_response(self, article: Article, quiz: Quiz) -> Dict[str, Any]:
        article_schema = ArticleInDB(
            id=article.id,
            url=article.url,
            title=article.title,
            summary=article.summary,
            sections=article.sections,
            entities=article.entities,
            created_at=article.created_at,
        )
        quiz_data = QuizData.model_validate(quiz.quiz_data)
        return {
            "article": article_schema.model_dump(),
            "quiz": quiz_data.model_dump(),
            "related_topics": quiz.related_topics or [],
        }

    # ---------------------------
    # History helpers
    # ---------------------------

    def list_quizzes(self) -> List[Dict[str, Any]]:
        stmt = (
            select(Quiz, Article)
            .join(Article, Quiz.article_id == Article.id)
            .order_by(Quiz.id.desc())
        )
        rows = self.db.execute(stmt).all()
        results: List[Dict[str, Any]] = []
        for quiz, article in rows:
            results.append(
                {
                    "id": quiz.id,
                    "article_id": article.id,
                    "article_title": article.title,
                    "article_url": article.url,
                    "created_at": article.created_at,
                }
            )
        return results

    def get_quiz_by_id(self, quiz_id: int) -> Optional[Dict[str, Any]]:
        stmt = (
            select(Quiz, Article)
            .join(Article, Quiz.article_id == Article.id)
            .where(Quiz.id == quiz_id)
        )
        row = self.db.execute(stmt).first()
        if not row:
            return None
        quiz, article = row
        quiz_data = QuizData.model_validate(quiz.quiz_data)
        article_schema = ArticleInDB(
            id=article.id,
            url=article.url,
            title=article.title,
            summary=article.summary,
            sections=article.sections,
            entities=article.entities,
            created_at=article.created_at,
        )
        return {
            "id": quiz.id,
            "article": article_schema.model_dump(),
            "quiz": quiz_data.model_dump(),
            "related_topics": quiz.related_topics or [],
        }

