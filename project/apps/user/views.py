from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.user.models import User
from apps.user.serializers import UserCreate
from apps.user.serializers import UserRead
from core.db import get_db_session

v1 = APIRouter()


@v1.get("/users/{uid}", response_model=UserRead)
def get_user(uid: int, db_session: Session = Depends(get_db_session)) -> User:
    user = db_session.get(User, uid)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@v1.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def add_user(user: UserCreate, db_session: Session = Depends(get_db_session)) -> User:
    instance = User(name=user.name)
    db_session.add(instance)
    db_session.commit()
    db_session.refresh(instance)
    return instance


@v1.delete("/users/{uid}")
def delete_user(uid: int, db_session: Session = Depends(get_db_session)) -> dict[str, int]:
    user = db_session.get(User, uid)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_session.delete(user)
    db_session.commit()
    return {"id": uid}
