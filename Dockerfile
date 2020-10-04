FROM python:3.8 as build
ENV PYTHONPATH /opt/application/
ENV PATH /opt/application/:$PATH
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.5

WORKDIR /opt/application/

RUN mkdir -p /root/.ssh && chmod 0700 /root/.ssh
COPY dp_keys/ /root/.ssh/
RUN chmod -R 600 /root/.ssh/.*

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
COPY poetry.lock .
COPY pyproject.toml  .
RUN poetry install --no-dev --no-root

FROM python:3.8-slim as project
COPY --from=build /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages
COPY --from=build /usr/local/bin/gunicorn /usr/local/bin/gunicorn

RUN useradd -g users user
USER user
WORKDIR /opt/application/

ENV PYTHONPATH /usr/local/lib/python3.8/site-packages:/opt/application/

COPY project /opt/application/
COPY gunicorn.conf.py /opt/application/
CMD gunicorn -c gunicorn.conf.py -b 0.0.0.0:8000 --log-level debug --access-logfile "-" --error-logfile "-" asgi:app
