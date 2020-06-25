import uuid

from pydantic import BaseConfig
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy.orm import sessionmaker

from core.settings import settings
from gino import create_engine
from gino.declarative import declared_attr

from . import db

engine = create_engine(
    settings.DB_DSN, echo=True, connect_args={"check_same_thread": False}
)

Session = sessionmaker(bind=engine)


class PydanticConfig(BaseConfig):
    orm_mode = True


class BaseDBModel(db.Model):
    __abstract__ = True
    _model = None
    readable_field = "id"

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def model(cls):
        if not cls._model:
            cls._model = sqlalchemy_to_pydantic(
                cls, config=PydanticConfig, exclude=["id"]
            )
        return cls._model

    def __repr__(self):
        return f"<{self.__class__.__name__}: {getattr(self, self.readable_field)}>"
