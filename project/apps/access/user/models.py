from core.server.db import db
from core.server.db.base import Base
from . import app_name


class User(Base):
    """Модель для управления пользователями."""
    __tablename__ = f'{app_name}.user'

    name = db.Column(db.Unicode(), default="unnamed")
