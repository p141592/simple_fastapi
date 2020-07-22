from fastapi import APIRouter

from .models import User
from .serializers import UserModel

v1 = APIRouter()


@v1.get("/users/{uid}")
async def get_user(uid: int):
    user = await User.get_or_404(uid)
    return user.to_dict()


@v1.post("/users")
async def add_user(user: UserModel):
    rv = await User.create(name=user.name)
    return rv.to_dict()


@v1.delete("/users/{uid}")
async def delete_user(uid: int):
    user = await User.get_or_404(uid)
    await user.delete()
    return dict(id=uid)
