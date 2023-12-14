from sqlalchemy.orm import mapped_column
import bcrypt
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

    def set_password(self, password: str) -> None:
        pw = bytes(password, "utf-8")
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(pw, salt)

    def check_password(self, password: str) -> bool:
        password_bytes = bytes(password, "utf-8")
        return bcrypt.checkpw(password_bytes, self.password)
