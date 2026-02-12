from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, HttpUrl


class EntitySummary(BaseModel):
    people: List[str] = []
    organizations: List[str] = []
    locations: List[str] = []


class ScrapedArticleContent(BaseModel):
    url: HttpUrl
    title: str
    summary: Optional[str] = None
    sections: List[Dict[str, Any]]
    text: str
    raw_html: str
    entities: EntitySummary


class ArticleBase(BaseModel):
    url: HttpUrl


class ArticleCreate(ArticleBase):
    title: str
    summary: Optional[str] = None
    sections: Optional[Dict[str, Any]] = None
    entities: Optional[Dict[str, Any]] = None
    raw_html: str


class ArticleInDB(ArticleBase):
    id: int
    title: str
    summary: Optional[str] = None
    sections: Optional[Dict[str, Any]] = None
    entities: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

