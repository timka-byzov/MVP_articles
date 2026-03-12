from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import settings

# Синхронный engine для создания таблиц
sync_engine = create_engine(settings.DATABASE_URL, echo=True)

# Async engine для FastAPI Users
async_database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(async_database_url, echo=True)

# Async session maker
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


def create_db_and_tables():
    # Импортируем все модели чтобы они зарегистрировались в metadata
    from app.models.user import User
    from app.models import Article, UserInteraction, UserPreference
    
    # Создаем все таблицы синхронно при старте
    SQLModel.metadata.create_all(sync_engine)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


# Для обратной совместимости с другими endpoints
def get_session():
    from sqlmodel import Session
    session = Session(sync_engine)
    try:
        yield session
    finally:
        session.close()