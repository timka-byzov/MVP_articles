from fastapi_users import schemas
from uuid import UUID
from typing import Optional
from pydantic import field_validator


class UserRead(schemas.BaseUser[UUID]):
    full_name: Optional[str]


class UserCreate(schemas.BaseUserCreate):
    full_name: Optional[str]
    
    @field_validator('password', mode='before')
    @classmethod
    def truncate_password(cls, v: str) -> str:
        """Truncate password to 72 bytes for bcrypt compatibility"""
        if isinstance(v, str):
            password_bytes = v.encode('utf-8')
            if len(password_bytes) > 72:
                # Truncate to 72 bytes and decode back
                return password_bytes[:72].decode('utf-8', errors='ignore')
        return v


class UserUpdate(schemas.BaseUserUpdate):
    full_name: Optional[str]