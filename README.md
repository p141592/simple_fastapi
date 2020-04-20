# Simple FastAPI project

Пример проекта на [fastapi](https://github.com/tiangolo/fastapi)

**Для работы требуется Python 3.8. Достаточно его просто установить в систему, при запуске poetry сам найдет 
исполняемый файл**

https://www.python.org/downloads/release/python-382/ или `apt install python3.8`

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

Запуск: `make activate && make run`

Миграции: `make makemigrations`, `make migrate`
