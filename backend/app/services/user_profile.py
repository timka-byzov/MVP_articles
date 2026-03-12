from sqlmodel import Session, select
from app.models.interaction import UserInteraction
from app.models.preference import UserPreference
from app.models.article import Article
from uuid import UUID
from datetime import datetime, timedelta


class UserProfileService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_recent_interactions(
        self,
        user_id: UUID,
        days: int = 30
    ) -> list[tuple[UserInteraction, Article]]:
        """Получить недавние взаимодействия с загруженными статьями"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        statement = (
            select(UserInteraction, Article)
            .join(Article, UserInteraction.article_id == Article.id)
            .where(
                UserInteraction.user_id == user_id,
                UserInteraction.created_at >= cutoff_date
            )
        )
        return list(self.session.exec(statement).all())
    
    def get_preferences(self, user_id: UUID) -> list[UserPreference]:
        """Получить предпочтения пользователя"""
        statement = select(UserPreference).where(
            UserPreference.user_id == user_id
        )
        return list(self.session.exec(statement).all())
    
    def get_interacted_article_ids(self, user_id: UUID) -> list[UUID]:
        """Получить ID статей с которыми взаимодействовал пользователь"""
        statement = select(UserInteraction.article_id).where(
            UserInteraction.user_id == user_id
        )
        return [row for row in self.session.exec(statement).all()]
    
    def get_hidden_article_ids(self, user_id: UUID) -> list[UUID]:
        """Получить ID скрытых статей"""
        from app.models.interaction import InteractionType
        statement = select(UserInteraction.article_id).where(
            UserInteraction.user_id == user_id,
            UserInteraction.interaction_type == InteractionType.HIDE
        )
        return [row for row in self.session.exec(statement).all()]