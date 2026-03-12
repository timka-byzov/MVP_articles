from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class UserPreference(SQLModel, table=True):
    __tablename__ = "userpreference"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    topic: str = Field(index=True)
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)