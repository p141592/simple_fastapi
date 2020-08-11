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
	PYTHONPATH=$(shell pwd)/project poetry run pytest --cov=project --cov-report=term-missing --cov-report=xml -vv ${TEST_CASE}

lock:
	poetry lock

linter:
	PYTHONPATH=$(shell pwd)/project poetry run black .

build: test linter
	docker build -t ${IMG}:${TAG} .

makemigrations:
	PYTHONPATH=$(shell pwd)/project poetry run alembic revision --autogenerate

migrate:
	PYTHONPATH=$(shell pwd)/project poetry run alembic upgrade head

downgrade:
	PYTHONPATH=$(shell pwd)/project poetry run alembic downgrade -1

fixtures:
	# TODO: Загрузка фикстур из JSON

run:
	PYTHONPATH=$(shell pwd)/project poetry run uvicorn project.asgi:app --reload

push: lock build
	docker push ${IMG}:${TAG}

dp-keys:
	ssh-keygen -t rsa -b 4096 -C "${PROJECT_NAME}@simple_fastapi" -f $(shell pwd)/dp_keys/id_rsa
	chmod 600 $(shell pwd)/dp_keys/*
	chmod 0700 $(shell pwd)/dp_keys/

dp-host:
	ssh-keyscan -H ${SSH_HOST} >> $(shell pwd)/dp_keys/known_hosts

logs:
	k logs -f -l app=${PROJECT_NAME} --all-containers=true

watch:
	# Для этого нужно установить `watch`: `brew install watch`
	watch -n 1 kubectl get all -l app=${PROJECT_NAME} -A

k8s-apply: push
	kubectl -n ${PROJECT_NAMESPACE} patch deployment ${DEPLOYMENT_NAME} --patch '{"spec": {"template": {"spec": {"containers": [{"name": "${PROJECT_NAME}","image": "${IMG}:${TAG}"}]}}}}'

helm:
	# TODO: Деплой helm чарта

gcloud-deploy: push
	gcloud run deploy ${PROJECT_NAME} --image ${IMG}:${TAG} --memory ${MEMORY_LIMIT} --platform managed --set-env-vars ${ENV_VARIABLES}

gcloud-remove:
	gcloud run service delete ${PROJECT_NAME}
