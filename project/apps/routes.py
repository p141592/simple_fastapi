from apps.user.views import v1
from fastapi import APIRouter

router = APIRouter()

router.include_router(v1, prefix="/user/v1", tags=["user"])
