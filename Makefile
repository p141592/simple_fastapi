DOCKER_REGISTRY = gcr.io/${GCLOUD-PROJECT-ID}
PORTS = 8080:8080

PROJECT_NAME = simple-fastapi
GCLOUD-PROJECT-ID = home-260209
PROJECT_NAMESPACE = default
DEPLOYMENT_NAME = ${PROJECT_NAME}

ENV = dev
MEMORY_LIMIT = 50M
ENV_VARIABLES = $(shell ./utils/convert_env.py $(shell pwd)/.env)

REPO_PATH := $(shell git rev-parse --show-toplevel)
CHANGED_FILES := $(shell git diff-files)

ifeq ($(strip $(CHANGED_FILES)),)
GIT_VERSION := $(shell git describe --tags --long --always)
else
GIT_VERSION := $(shell git describe --tags --long --always)-dirty-$(shell git diff | shasum -a256 | cut -c -6)
endif

IMG ?= ${DOCKER_REGISTRY}/${PROJECT_NAME}
TAG ?= $(GIT_VERSION)

activate: 
	pip install --user poetry
	poetry install --no-root

test:
	PYTHONPATH=$(shell pwd)/project poetry run pytest -vv ${TEST_CASE}

lock:
	poetry lock

linter:
	PYTHONPATH=$(shell pwd)/project poetry run black .

# pre production
build: test linter
	docker build -t ${IMG}:${TAG} .

makemigrations:
	PYTHONPATH=$(shell pwd)/project poetry run alembic revision --autogenerate

migrate:
	PYTHONPATH=$(shell pwd)/project poetry run alembic upgrade head

downgrade:
	PYTHONPATH=$(shell pwd)/project poetry run alembic downgrade -1

run:
	PYTHONPATH=$(shell pwd)/project poetry run uvicorn project.asgi:app --reload

push: build
	docker push ${IMG}:${TAG}

# TODO: Добавить генерацию манифеста

# TODO: Добавить чтение логов из кубера по проекту

watch:
	watch -n 1 kubectl -l app=${PROJECT_NAME} -A
# TODO: Добавить наблюдение за сервисом в кубере `-w`

k8s-apply: push
	kubectl -n ${PROJECT_NAMESPACE} patch deployment ${DEPLOYMENT_NAME} --patch '{"spec": {"template": {"spec": {"containers": [{"name": "${PROJECT_NAME}","image": "${IMG}:${TAG}"}]}}}}'

# TODO: Сделать deploy

# TODO: Добавить генерацию helm чарта

# deploy
gcloud-deploy: push
	gcloud run deploy ${PROJECT_NAME} --image ${IMG}:${TAG} --memory ${MEMORY_LIMIT} --platform managed --set-env-vars ${ENV_VARIABLES}

gcloud-remove:
	gcloud run service delete ${PROJECT_NAME}
