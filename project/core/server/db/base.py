import uuid

from gino.declarative import declared_attr

from . import db


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = db.Column(primary_key=True, unique=True, default=uuid.uuid4())
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
