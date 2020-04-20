# Simple FastAPI project

Пример проекта на [fastapi](https://github.com/tiangolo/fastapi)

Стек:

- [fastapi](https://github.com/tiangolo/fastapi)
- [gino](https://github.com/python-gino/gino) + [sqlalchemy](https://www.sqlalchemy.org/)
- [alembic](https://alembic.sqlalchemy.org/en/latest/)
- [poetry](https://github.com/python-poetry/poetry)
- postgresql
- docker

Интеграции:

- Сбор метрик Prometheus
- Sentry
- [Google Cloud Run](https://cloud.google.com/run)

TODO:

- Добавить обработчики ошибок
- Добавить логгирование
- Подключить создание временной базы на тестах
- JWT авторизация пользователя
