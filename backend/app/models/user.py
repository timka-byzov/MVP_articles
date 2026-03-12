from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional
import uuid


# Используем metadata из SQLModel для совместимости
class Base(DeclarativeBase):
    metadata = SQLModel.metadata


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
