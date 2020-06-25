import os

from fastapi import APIRouter

from prometheus_client.openmetrics.exposition import generate_latest
from prometheus_client.registry import CollectorRegistry

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    generate_latest,
    REGISTRY,
)
from prometheus_client.multiprocess import MultiProcessCollector
from starlette.requests import Request
from starlette.responses import Response

route = APIRouter()


@route.get("/metrics")
def metrics(request: Request) -> Response:
    if "prometheus_multiproc_dir" in os.environ:
        registry = CollectorRegistry()
        MultiProcessCollector(registry)
    else:
        registry = REGISTRY

    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)
