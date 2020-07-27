from core.db import db
from core.db.base import BaseDBModel


class User(BaseDBModel):
    """Модель для управления пользователями."""

    name = db.Column(db.Unicode())
