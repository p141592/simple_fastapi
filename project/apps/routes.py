from fastapi import APIRouter

from apps.user.views import v1

router = APIRouter()

router.include_router(v1, prefix="/user/v1", tags=["user"])
