from fastapi import APIRouter

from apps.access.user.views import v1

access = APIRouter()

access.include_router(v1, prefix="/user/v1", tags=["user"])
