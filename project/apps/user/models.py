from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import BaseDBModel


class User(BaseDBModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
