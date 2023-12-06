from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    UUID,
    DateTime,
    ForeignKey,
)

from src.database import Base


class BlacklistedToken(Base):
    __tablename__ = 'blacklisted_tokens'

    jti = mapped_column(UUID, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    expires_at = mapped_column(DateTime, nullable=False)
