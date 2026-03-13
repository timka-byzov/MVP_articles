from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, col
from app.models.user import User
from app.models.article import Article
from app.models.interaction import UserInteraction
from app.api.auth import current_active_user
from app.database import get_session
from app.services.recommender_cache import RecommenderCache
from app.services.user_profile import UserProfileService
from typing import List, Dict
from uuid import UUID


router = APIRouter(prefix="/api/feed", tags=["feed"])


@router.get("/")
async def get_feed(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(current_active_user),
    session: Session = Depends(get_session)
):
    """Получить персонализированную ленту"""
    
    # Получаем профиль пользователя
    profile_service = UserProfileService(session)
    interactions = profile_service.get_recent_interactions(user.id)
    preferences = profile_service.get_preferences(user.id)
    # Исключаем только скрытые статьи, а не все взаимодействия
    exclude_ids = profile_service.get_hidden_article_ids(user.id)
    
    # Получаем закэшированный рекомендатель
    recommender = RecommenderCache.get_recommender(session)
    
    if recommender is None:
        return {
            "articles": [],
            "total": 0,
            "limit": limit,
            "offset": offset
        }
    
    # Строим профиль пользователя
    user_profile = recommender.build_user_profile(interactions, preferences)
    
    # Получаем рекомендации
    recommended_ids = recommender.recommend(
        user_profile,
        n=limit + offset,
        exclude_ids=exclude_ids
    )
    
    # Применяем пагинацию
    page_ids = recommended_ids[offset:offset + limit]
    
    # Получаем статьи
    recommended_articles = []
    for article_id in page_ids:
        article = session.get(Article, article_id)
        if article:
            recommended_articles.append(article)
    
    # Получаем взаимодействия пользователя для этих статей
    user_interactions_map: Dict[UUID, Dict[str, bool]] = {}
    if page_ids:
        statement = select(UserInteraction).where(
            UserInteraction.user_id == user.id,
            col(UserInteraction.article_id).in_(page_ids)
        )
        user_interactions_list = session.exec(statement).all()
        
        for interaction in user_interactions_list:
            if interaction.article_id not in user_interactions_map:
                user_interactions_map[interaction.article_id] = {}
            user_interactions_map[interaction.article_id][interaction.interaction_type.value] = True
    
    # Формируем ответ с информацией о взаимодействиях
    articles_with_interactions = []
    for article in recommended_articles:
        article_dict = article.model_dump()
        article_dict['interactions'] = user_interactions_map.get(article.id, {})
        articles_with_interactions.append(article_dict)
    
    return {
        "articles": articles_with_interactions,
        "total": len(recommended_ids),
        "limit": limit,
        "offset": offset
    }