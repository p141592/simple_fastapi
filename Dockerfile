FROM python:3.7 AS build-env

COPY requirements.pip .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.pip

# Собираю инстанс самого проекта
FROM python:3.7-slim as project
COPY --from=build-env /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages

COPY ./src /opt/application/
COPY entrypoint.sh /opt/application/
ENV PATH /opt/application/:$PATH

WORKDIR /opt/application/

ENV PYTHONPATH /usr/local/lib/python3.7/site-packages
ENV PYTHONPATH /opt/application/

CMD entrypoint.sh

