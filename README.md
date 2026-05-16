# Simple FastAPI

<p align="center">
  <img src="https://cdn.simpleicons.org/fastapi/009688" alt="FastAPI" height="48">
  &nbsp;&nbsp;&nbsp;
  <img src="https://cdn.simpleicons.org/sqlalchemy/D71F00" alt="SQLAlchemy" height="48">
</p>

<p align="center">
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.135.3-009688?logo=fastapi&logoColor=white" alt="FastAPI 0.135.3"></a>
  <a href="https://www.sqlalchemy.org/"><img src="https://img.shields.io/badge/SQLAlchemy-2.0.49-D71F00?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy 2.0.49"></a>
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white" alt="pytest">
  <img src="https://img.shields.io/badge/license-MIT-111827" alt="MIT license">
</p>

Лаконичный backend-шаблон на FastAPI для сервисов, которым сразу нужны база данных,
миграции, healthcheck, метрики, статические файлы и понятная структура проекта.

![FastAPI application preview](docs/index.png)

## Что внутри

- FastAPI-приложение с единым factory-подходом в `project/core/application.py`
- SQLAlchemy 2.0 и Alembic для схемы базы данных
- PostgreSQL как основное хранилище
- Pydantic v2 и `pydantic-settings` для схем и конфигурации
- Prometheus endpoint `/metrics`
- Healthcheck endpoint `/healthz`
- Sentry middleware при наличии `SENTRY_DSN`
- Раздача `/static` и `/media`
- Пример CRUD API для пользователей
- Pytest, coverage и Black через Makefile
- Docker, Kubernetes и Google Cloud Run заготовки

## Структура

```text
project/
  apps/                 # Доменные модули и HTTP-роуты
    user/               # Пример user CRUD
  core/                 # Настройки, приложение, база, service endpoints
  static/               # Статические файлы
  media/                # Пользовательские/медийные файлы
  templates/            # Jinja2 templates
migrations/             # Alembic migrations
tests/                  # Pytest suite
utils/                  # Вспомогательные скрипты
```

## Требования

- Python `>=3.11,<3.15`
- Poetry
- PostgreSQL

По умолчанию приложение ждёт базу на:

```text
postgresql://postgres:postgres@localhost:5431/postgres
```

## Быстрый старт

```bash
make activate
make migrate
make run
```

После запуска:

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/healthz`
- Metrics: `http://localhost:8000/metrics`

Если база не запущена локально, поднимите PostgreSQL через Docker Compose:

```bash
docker compose up -d db
```

## Конфигурация

Настройки читаются из `.env` в корне репозитория и переменных окружения.

| Переменная | Значение по умолчанию | Назначение |
| --- | --- | --- |
| `HOST` | `0.0.0.0` | Адрес HTTP-сервера |
| `PORT` | `8000` | Порт приложения |
| `LOG_LEVEL` | `debug` | Уровень логирования Uvicorn |
| `RELOAD` | `False` | Автоперезапуск в dev-режиме |
| `SENTRY_DSN` | `None` | DSN для Sentry |
| `DB_DSN` | `postgresql://postgres:postgres@localhost:5431/postgres` | Подключение к PostgreSQL |
| `DB_ECHO` | `False` | SQLAlchemy query logging |

## API пример

Создать пользователя:

```bash
curl -X POST http://localhost:8000/user/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
```

Получить пользователя:

```bash
curl http://localhost:8000/user/v1/users/1
```

Удалить пользователя:

```bash
curl -X DELETE http://localhost:8000/user/v1/users/1
```

## Команды разработки

```bash
make test          # pytest + coverage
make linter        # black .
make makemigrations
make migrate
make downgrade
make build         # test + linter + docker build
```

## Миграции

Создать новую миграцию:

```bash
make makemigrations
```

Применить все миграции:

```bash
make migrate
```

Откатить последнюю:

```bash
make downgrade
```

## Тесты

```bash
make test
```

Тестовый набор проверяет:

- `/healthz`
- `/metrics`
- раздачу static/media
- базовый user CRUD
- Alembic migration runner
- utility-функции

## Деплой

В репозитории есть заготовки для контейнерного запуска и облачного деплоя:

- `Dockerfile`
- `docker-compose.yml`
- `k8s/deployment.yaml`
- `k8s/service-account.yaml`
- `make gcloud-deploy`

Перед production-запуском проверьте переменные окружения, доступность PostgreSQL,
Sentry DSN и актуальность Docker runtime под версию Python из `pyproject.toml`.

## FAQ

**Ошибка подключения к базе или сообщение, что database не существует**

Проверьте, что PostgreSQL запущен, база существует, а `DB_DSN` указывает на правильный
host, port, user, password и database.

**Poetry выбрал не ту версию Python**

Проверьте окружение:

```bash
poetry env info
```

Выберите подходящий интерпретатор:

```bash
poetry env use 3.11
```

**Приложение запускается из IDE, но не видит модули**

Укажите `PYTHONPATH` на папку `project` или используйте Makefile-команды. Для ручного
запуска entrypoint находится в `project/core/application.py`, ASGI-приложение — в
`project/asgi.py`.
