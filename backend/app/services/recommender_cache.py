from app.services.recommender import TFIDFRecommender
from app.models.article import Article
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime, timedelta


class RecommenderCache:
    """Singleton кэш для рекомендательной системы"""
    _instance: Optional[TFIDFRecommender] = None
    _last_update: Optional[datetime] = None
    _cache_duration = timedelta(minutes=30)  # Обновлять каждые 30 минут
    
    @classmethod
    def get_recommender(cls, session: Session) -> TFIDFRecommender:
        """Получить закэшированный рекомендатель"""
        now = datetime.utcnow()
        
        # Проверяем нужно ли обновить кэш
        if (cls._instance is None or 
            cls._last_update is None or 
            now - cls._last_update > cls._cache_duration):
            
            # Загружаем все статьи
            articles = list(session.exec(select(Article)).all())
            
            if articles:
                # Создаем и обучаем рекомендатель
                cls._instance = TFIDFRecommender()
                cls._instance.fit(articles)
                cls._last_update = now
        
        return cls._instance
    
    @classmethod
    def invalidate(cls):
        """Сбросить кэш (вызывать после импорта новых статей)"""
        cls._instance = None
        cls._last_update = None