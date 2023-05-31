from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    Boolean,
    String,
    LargeBinary,
    UUID,
    DateTime,
    ForeignKey
)

from src.database import Base


class User(Base):
    __tablename__ = "users"

    username = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(LargeBinary, nullable=False)
    is_admin = mapped_column(Boolean, default=False, server_default="false", nullable=False)


class WhitelistedToken(Base):
    __tablename__ = 'whitelisted_tokens'

    jti = mapped_column(UUID, unique=True)
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    expires_at = mapped_column(DateTime, nullable=False)
