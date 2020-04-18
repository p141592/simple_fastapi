from core.server.db import db
from . import app_name


class User(db.Model):
    """Модель для управления пользователями."""
    __tablename__ = f'{app_name}.user'

    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.Unicode(), default="unnamed")
