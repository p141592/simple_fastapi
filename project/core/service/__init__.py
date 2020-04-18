from fastapi import APIRouter

from core.service.healthz import route as healthz
from core.service.metrics import route as metrics

service_route = APIRouter()

service_route.include_router(healthz)
service_route.include_router(metrics)
