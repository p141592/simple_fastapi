from core.server.db import db
from core.server.db.base import BaseDBModel


class User(BaseDBModel):
    """Модель для управления пользователями."""

    name = db.Column(db.Unicode(), default="unnamed")
