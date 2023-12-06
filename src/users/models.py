from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    Boolean,
    String,
    LargeBinary,
    Integer
)

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(LargeBinary, nullable=False)
    is_admin = mapped_column(Boolean, default=False, server_default="false", nullable=False)
