from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.user import User
from app.models.preference import UserPreference
from app.api.auth import current_active_user
from app.database import get_session
from pydantic import BaseModel
from typing import List


router = APIRouter(prefix="/api/preferences", tags=["preferences"])


class TopicPreference(BaseModel):
    topic: str
    weight: float = 1.0


class PreferencesCreate(BaseModel):
    topics: List[TopicPreference]


@router.post("/")
async def set_preferences(
    preferences: PreferencesCreate,
    user: User = Depends(current_active_user),
    session: Session = Depends(get_session)
):
    """Установить предпочтения пользователя"""
    # Удаляем старые предпочтения
    statement = select(UserPreference).where(UserPreference.user_id == user.id)
    old_prefs = list(session.exec(statement).all())
    for pref in old_prefs:
        session.delete(pref)
    
    # Создаем новые
    new_prefs = []
    for topic_pref in preferences.topics:
        pref = UserPreference(
            user_id=user.id,
            topic=topic_pref.topic,
            weight=topic_pref.weight
        )
        session.add(pref)
        new_prefs.append(pref)
    
    session.commit()
    
    # Обновляем объекты
    for pref in new_prefs:
        session.refresh(pref)
    
    return {"status": "success", "preferences": new_prefs}


@router.get("/")
async def get_preferences(
    user: User = Depends(current_active_user),
    session: Session = Depends(get_session)
):
    """Получить предпочтения пользователя"""
    statement = select(UserPreference).where(UserPreference.user_id == user.id)
    preferences = list(session.exec(statement).all())
    return {"preferences": preferences}