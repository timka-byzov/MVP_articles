from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
import enum


class InteractionType(str, enum.Enum):
    VIEW = "view"
    LIKE = "like"
    SAVE = "save"
    HIDE = "hide"


class UserInteraction(SQLModel, table=True):
    __tablename__ = "userinteraction"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    article_id: UUID = Field(foreign_key="article.id", index=True)
    interaction_type: InteractionType
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)