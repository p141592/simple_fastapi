# Simple FastAPI project

Пример проекта на [fastapi](https://github.com/tiangolo/fastapi)

**Для работы требуется Python 3.8. Достаточно его просто установить в систему, при запуске poetry сам найдет 
исполняемый файл**

https://www.python.org/downloads/release/python-382/ или `apt install python3.8`

![](docs/index.png)

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

Запуск: `make activate && make run`

Миграции: `make makemigrations`, `make migrate`

## TODO:

- Добавить обработчики ошибок
- Добавить логгирование
- JWT авторизация пользователя
- Использование celery через rabbitmq
- Кеш на keydb
- Добавить возможность создавать текстовую документацию и хранить вместе с проектом


## FAQ

Ошибка: `asyncpg.exceptions.InvalidCatalogNameError: database "gino" does not exist`

Не создана база `gino`. Это база, указанная по умолчанию в проекте. 
Все настройки проекта меняются в файле `project/settings.py`, так же в файле `.env` в корне проекта

## Запуск проекта локально:

- `poetry install` 
- PYTHONPATH=$(pwd)/project
- `make run`

Если выхотите запустить проект из IDE, следует указать путь до `project/core/application.py`
