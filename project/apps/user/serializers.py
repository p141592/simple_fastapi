import uuid

from pydantic import BaseModel


class UserModel(BaseModel):
    id: uuid.UUID = None
    name: str
