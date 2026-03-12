from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime, date
from uuid import UUID, uuid4
from typing import Optional, List


class Article(SQLModel, table=True):
    __tablename__ = "article"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(index=True)
    abstract: str
    summary: str
    authors: dict = Field(sa_column=Column(JSON))
    source: str = Field(index=True)
    doi: Optional[str] = None
    publication_date: date
    topics: List[str] = Field(default=[], sa_column=Column(JSON))
    url: Optional[str] = None
    tfidf_vector: Optional[str] = None  # Сериализованный numpy array
    created_at: datetime = Field(default_factory=datetime.utcnow)