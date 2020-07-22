import sqlalchemy as s
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util.compat import contextmanager
from pydantic import BaseConfig

from core.settings import settings

engine = create_engine(
    settings.DB_DSN, echo=True, connect_args={"check_same_thread": False}
)

Base = declarative_base()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class PydanticConfig(BaseConfig):
    orm_mode = True


class BaseDBModel(Base):
    __abstract__ = True
    _model = None
    readable_field = "id"

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = s.Column(s.Integer, primary_key=True, unique=True, autoincrement=True)

    @classmethod
    def model(cls, **kwargs):
        return sqlalchemy_to_pydantic(cls, config=PydanticConfig, **kwargs)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {getattr(self, self.readable_field)}>"


class BaseDBHandbook(BaseDBModel):
    __abstract__ = True
    readable_field = "title"

    title = s.Column(s.String)
    key = s.Column(s.String, nullable=False, unique=True)
