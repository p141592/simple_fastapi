# TODO: Перейти на alpine
FROM python:3.8
ENV PYTHONPATH /opt/application/
ENV PATH /opt/application/:$PATH
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.5

WORKDIR /opt/application/

# TODO: Добавить прокидывание deployment keys

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
COPY poetry.lock .
COPY pyproject.toml  .
RUN poetry install --no-dev --no-root

COPY project /opt/application/

# TODO: Создать пользователя и оставлять докер под ним

CMD python -m core.server
