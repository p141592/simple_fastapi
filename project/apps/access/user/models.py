import enum
import uuid

from sqlalchemy import String, Boolean
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, URLType

from apps.access.user import AbstractUser, DEFAULT_USER_SETTINGS
from core.db import BaseModel
from core.server import db


class UserStatus(enum.Enum):
    NORMAL = 'normal'
    BLOCK = 'blocked'
    RECOVERABLE = 'recoverable'
    DELETED = 'deleted'


class User(AbstractUser):
    """Модель для управления пользователями."""
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(EmailType, unique=True)
    tutorial_passed = db.Column(Boolean, default=False)

    settings = db.Column(JSONB, default=DEFAULT_USER_SETTINGS)
    status = db.Column(postgresql.ENUM('normal', 'blocked', 'recoverable', 'deleted', name='user_status'))

    profile = relationship("Profile", back_populates="user")
    company = relationship("Company", backref="user")

    creator = db.Column()


class Profile(db.Model):
    __tablename__ = 'profile'

    email = db.Column(EmailType, unique=True)
    firstname = db.Column(String)
    middlename = db.Column(String)
    lastname = db.Column(String)
    phone = db.Column(String)
    url = db.Column(URLType)
    user = relationship("User", uselist=False, back_populates="profile")


class Company(db.Model):
    __tablename__ = 'company'

    name = db.Column(String)
    form = db.Column(String)


class Invite(BaseModel):
    __tablename__ = 'invite'

    def code_generator(self):
        return 1

    email = db.Column(EmailType, unique=True)
    data = db.Column(JSONB)
    code = db.Column(String, default=code_generator)
    completed = db.Column(Boolean, default=False)
