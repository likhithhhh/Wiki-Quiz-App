import json
from pathlib import Path
from typing import Any, Dict, List

from google.api_core.exceptions import GoogleAPIError
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSerializable
from langchain_groq import ChatGroq

from app.config import get_settings
from app.schemas.article_schema import ScrapedArticleContent
from app.schemas.quiz_schema import QuizData

settings = get_settings()
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"


class LLMError(RuntimeError):
    """Raised when the LLM response cannot be parsed or is invalid."""


def _load_prompt(name: str) -> str:
    """Load a prompt template by filename from the prompts directory."""
    prompt_path = PROMPTS_DIR / name
    return prompt_path.read_text(encoding="utf-8")


def _build_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=settings.GROQ_API_KEY,
        temperature=0.3,
    )



def build_quiz_chain() -> RunnableSerializable:
    """Chain that generates quiz JSON from article content."""
    template_str = _load_prompt("quiz_prompt.txt")
    prompt = PromptTemplate.from_template(
        template_str
        + "\n\nARTICLE TITLE:\n{title}\n\nSUMMARY:\n{summary}\n\nSECTIONS:\n{sections}\n\nENTITIES:\n{entities}\n\nFULL TEXT:\n{text}\n"
    )
    llm = _build_llm()
    return prompt | llm


def build_related_topics_chain() -> RunnableSerializable:
    """Chain that generates related topics JSON from article content."""
    template_str = _load_prompt("related_topics_prompt.txt")
    prompt = PromptTemplate.from_template(
        template_str
        + "\n\nARTICLE TITLE:\n{title}\n\nSUMMARY:\n{summary}\n\nSECTIONS:\n{sections}\n\nFULL TEXT:\n{text}\n"
    )
    llm = _build_llm()
    return prompt | llm


def _safe_json_parse(content: str) -> Dict[str, Any]:
    """Attempt to parse JSON from an LLM response, stripping code fences if present."""
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        # Remove leading language hints like ```json
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned)


def generate_quiz_and_topics(article: ScrapedArticleContent) -> Dict[str, Any]:
    """Call Gemini via LangChain to generate quiz questions and related topics."""
    quiz_chain = build_quiz_chain()
    topics_chain = build_related_topics_chain()

    common_input = {
        "title": article.title,
        "summary": article.summary or "",
        "sections": article.sections,
        "entities": article.entities.model_dump(),
        "text": article.text,
    }

    try:
        quiz_output = quiz_chain.invoke(common_input)
        topics_output = topics_chain.invoke(common_input)
    except GoogleAPIError as exc:  # pragma: no cover - external service
        raise LLMError(
            f"Gemini API call failed: {exc.message if hasattr(exc, 'message') else str(exc)}"
        ) from exc
    except Exception as exc:  # pragma: no cover
        raise LLMError(f"Unexpected error while calling Gemini: {exc}") from exc

    quiz_json = _safe_json_parse(
        quiz_output.content if hasattr(quiz_output, "content") else str(quiz_output)
    )
    topics_json = _safe_json_parse(
        topics_output.content if hasattr(topics_output, "content") else str(topics_output)
    )

    quiz = QuizData.model_validate(quiz_json)
    related_topics: List[str] = topics_json.get("topics", [])

    return {
        "quiz": quiz,
        "related_topics": related_topics,
    }


