from fastapi import APIRouter

from apps.access.routes import access

apps = APIRouter()

apps.include_router(access, prefix='/api/access', tags=['user'])
