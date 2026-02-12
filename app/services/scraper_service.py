from typing import List, Tuple

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from app.schemas.article_schema import EntitySummary, ScrapedArticleContent


WIKIPEDIA_DOMAIN = "wikipedia.org"


class InvalidWikipediaURLError(ValueError):
    """Raised when the provided URL is not a valid Wikipedia article."""


def validate_wikipedia_url(url: str) -> None:
    """Basic validation to ensure the URL is a Wikipedia article."""
    if WIKIPEDIA_DOMAIN not in url:
        raise InvalidWikipediaURLError("URL must be a Wikipedia article (contain 'wikipedia.org').")
    if any(path in url for path in ["/wiki/Special:", "/wiki/Talk:", "/wiki/Help:"]):
        raise InvalidWikipediaURLError("URL must be a standard article, not a special page.")


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=4))
def fetch_html(url: str) -> str:
    """Fetch raw HTML from the given URL with basic retries."""
    headers = {
        "User-Agent": "WikiQuizApp/1.0 (+https://github.com/your-org/wiki-quiz-app)",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def _extract_title(soup: BeautifulSoup) -> str:
    title_el = soup.find(id="firstHeading")
    if title_el and title_el.get_text(strip=True):
        return title_el.get_text(strip=True)
    if soup.title and soup.title.string:
        return soup.title.string.replace(" - Wikipedia", "").strip()
    return "Untitled Article"


def _extract_summary_and_sections(soup: BeautifulSoup) -> Tuple[str, List[dict], str]:
    """Extract the lead summary, sections, and full plain text."""
    content_div = soup.find("div", id="mw-content-text")
    if not content_div:
        return "", [], ""

    paragraphs = []
    sections: List[dict] = []
    current_section = {"title": "Introduction", "content": ""}

    for el in content_div.descendants:
        if el.name in ["h2", "h3"]:
            if current_section["content"].strip():
                sections.append(current_section)
            heading_text = el.get_text(" ", strip=True).replace("[edit]", "").strip()
            current_section = {"title": heading_text, "content": ""}
        elif el.name == "p":
            text = el.get_text(" ", strip=True)
            if text:
                paragraphs.append(text)
                current_section["content"] += text + "\n"

    if current_section["content"].strip():
        sections.append(current_section)

    full_text = "\n".join(paragraphs)
    summary = paragraphs[0] if paragraphs else ""
    return summary, sections, full_text


def scrape_wikipedia_article(url: str) -> ScrapedArticleContent:
    """Validate and scrape a Wikipedia article into structured content."""
    validate_wikipedia_url(url)
    raw_html = fetch_html(url)
    soup = BeautifulSoup(raw_html, "html.parser")

    title = _extract_title(soup)
    summary, sections, full_text = _extract_summary_and_sections(soup)

    # Entities will be filled by a separate service; placeholder here.
    entities = EntitySummary(people=[], organizations=[], locations=[])

    return ScrapedArticleContent(
        url=url,
        title=title,
        summary=summary,
        sections=sections,
        text=full_text,
        raw_html=raw_html,
        entities=entities,
    )

