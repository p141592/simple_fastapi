import uuid

from sqlalchemy.dialects.postgresql import UUID

from core.server.db import db


class User(db.Model):
    """Модель для управления пользователями."""
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
