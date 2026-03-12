from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserRead, UserCreate, UserUpdate
from app.config import settings
from app.database import get_async_session
from uuid import UUID
from typing import AsyncGenerator


# Cookie transport
cookie_transport = CookieTransport(
    cookie_name="auth_token",
    cookie_max_age=3600 * 24 * 7,
    cookie_secure=False,  # True в production
    cookie_httponly=True,
    cookie_samesite="lax"
)


# JWT Strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600 * 24 * 7)


# Auth backend
auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


# User database
async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, User)


# User manager
async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    from fastapi_users import BaseUserManager
    from fastapi_users.password import PasswordHelper
    import bcrypt
    
    class CustomPasswordHelper(PasswordHelper):
        def hash(self, password: str) -> str:
            # Обрезаем пароль до 72 байт для bcrypt
            password_bytes = password.encode('utf-8')[:72]
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)
            return hashed.decode('utf-8')
        
        def verify_and_update(self, plain_password: str, hashed_password: str):
            # Обрезаем пароль при проверке
            plain_password_bytes = plain_password.encode('utf-8')[:72]
            verified = bcrypt.checkpw(plain_password_bytes, hashed_password.encode('utf-8'))
            # bcrypt не требует обновления хеша
            return verified, None
    
    class UserManager(BaseUserManager[User, UUID]):
        reset_password_token_secret = settings.SECRET_KEY
        verification_token_secret = settings.SECRET_KEY
        
        def __init__(self, user_db):
            super().__init__(user_db)
            self.password_helper = CustomPasswordHelper()
        
        def parse_id(self, value: str) -> UUID:
            """Parse string ID to UUID"""
            return UUID(value)
        
        async def create(self, user_create, safe: bool = False, request = None):
            """Override create to truncate password before hashing"""
            # Truncate password to 72 bytes
            if hasattr(user_create, 'password') and user_create.password:
                password_bytes = user_create.password.encode('utf-8')
                if len(password_bytes) > 72:
                    user_create.password = password_bytes[:72].decode('utf-8', errors='ignore')
            
            return await super().create(user_create, safe=safe, request=request)
    
    yield UserManager(user_db)


# FastAPI Users instance
fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)


# Current user dependency
current_active_user = fastapi_users.current_user(active=True)


# Auth router
def get_auth_router():
    from fastapi import APIRouter
    
    router = APIRouter()
    
    # Include auth routes (login, logout)
    router.include_router(
        fastapi_users.get_auth_router(auth_backend),
        tags=["auth"]
    )
    
    # Include register routes
    router.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        tags=["auth"]
    )
    
    # Include users routes (me endpoint)
    router.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"]
    )
    
    return router