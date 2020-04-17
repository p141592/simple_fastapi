import logging
from asyncio import get_event_loop

import uvicorn
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from core import settings

logger = logging.getLogger(__name__)


class Application(FastAPI):
    __instance = None

    ORIGINS = [
        "http://localhost",
        "http://localhost:8000",
    ]

    def __init__(self):
        """Инициализация приложения компонентами"""
        super(Application, self).__init__(**settings.AppSettings().dict())

        self.mount(
            "/static",
            StaticFiles(directory=settings.STATIC_PATH),
            name="static",
        )
        self.mount(
            "/media", StaticFiles(directory=settings.MEDIA_PATH), name="media"
        )

        self.add_middleware(
            CORSMiddleware,
            allow_origins=self.ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @classmethod
    def run(cls, *args, **kwargs):
        """Вызывается для локального запуска
        Для локального запуска достаточно выполнить в корне проекта: `poetry run python -m project`

        Работает это следующим образом:
        При вызове пакета, python ищет файл __main__.py, в __main__.py вызывается этот метод для
        упращения процедуры запуска
        """
        uvicorn.run("project.asgi:app", **settings.RunSettings().dict())

    @property
    def loop(self):
        return get_event_loop()

