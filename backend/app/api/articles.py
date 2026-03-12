from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import User
from app.models.article import Article
from app.models.interaction import UserInteraction, InteractionType
from app.api.auth import current_active_user
from app.database import get_session
from pydantic import BaseModel
from uuid import UUID


router = APIRouter(prefix="/api/articles", tags=["articles"])


class InteractionCreate(BaseModel):
    interaction_type: InteractionType


@router.get("/saved/list")
async def get_saved_articles(
    user: User = Depends(current_active_user),
    session: Session = Depends(get_session)
):
    """Получить сохраненные статьи"""
    # Сначала получаем ID сохраненных статей
    statement = (
        select(UserInteraction.article_id)
        .where(
            UserInteraction.user_id == user.id,
            UserInteraction.interaction_type == InteractionType.SAVE
        )
        .distinct()
    )
    article_ids = list(session.exec(statement).all())
    
    # Загружаем сами статьи
    result_articles = []
    for article_id in article_ids:
        article = session.get(Article, article_id)
        if article:
            # Получаем все взаимодействия пользователя с этой статьей
            interactions_stmt = select(UserInteraction).where(
                UserInteraction.user_id == user.id,
                UserInteraction.article_id == article.id
            )
            user_interactions = session.exec(interactions_stmt).all()
            
            # Формируем словарь взаимодействий
            interactions_dict = {
                interaction.interaction_type.value: True
                for interaction in user_interactions
            }
            
            # Добавляем interactions к статье
            article_dict = article.model_dump()
            article_dict['interactions'] = interactions_dict
            result_articles.append(article_dict)
    
    return {"articles": result_articles}


@router.get("/liked/list")
async def get_liked_articles(
    user: User = Depends(current_active_user),
    session: Session = Depends(get_session)
):
    """Получить лайкнутые статьи"""
    # Сначала получаем ID лайкнутых статей
    statement = (
        select(UserInteraction.article_id)
        .where(
            UserInteraction.user_id == user.id,
            UserInteraction.interaction_type == InteractionType.LIKE
        )
        .distinct()
    )
    article_ids = list(session.exec(statement).all())
    
    # Загружаем сами статьи
    articles = []
    for article_id in article_ids:
        article = session.get(Article, article_id)
        if article:
            articles.append(article)
    
    return {"articles": articles}


@router.get("/{article_id}")
async def get_article(
    article_id: UUID,
    session: Session = Depends(get_session)
):
    """Получить статью по ID"""
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/{article_id}/interact")
async def interact_with_article(
    article_id: UUID,
    interaction: InteractionCreate,
    user: User = Depends(current_active_user),
    session: Session = Depends(get_session)
):
    """Взаимодействие со статьей (toggle для like/save, permanent для hide)"""
    # Проверяем существование статьи
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Проверяем, есть ли уже такое взаимодействие
    statement = select(UserInteraction).where(
        UserInteraction.user_id == user.id,
        UserInteraction.article_id == article_id,
        UserInteraction.interaction_type == interaction.interaction_type
    )
    existing = session.exec(statement).first()
    
    # HIDE не имеет toggle - только добавление
    if interaction.interaction_type == InteractionType.HIDE:
        if not existing:
            user_interaction = UserInteraction(
                user_id=user.id,
                article_id=article_id,
                interaction_type=interaction.interaction_type
            )
            session.add(user_interaction)
            session.commit()
            session.refresh(user_interaction)
        return {"status": "added", "interaction_type": interaction.interaction_type}
    
    # Для LIKE и SAVE - toggle behavior
    if existing:
        # Если взаимодействие уже есть - удаляем (toggle off)
        session.delete(existing)
        session.commit()
        return {"status": "removed", "interaction_type": interaction.interaction_type}
    else:
        # Создаем новое взаимодействие
        user_interaction = UserInteraction(
            user_id=user.id,
            article_id=article_id,
            interaction_type=interaction.interaction_type
        )
        session.add(user_interaction)
        session.commit()
        session.refresh(user_interaction)
        return {"status": "added", "interaction": user_interaction}