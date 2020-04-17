# Registry where you want store your Docker images
DOCKER_REGISTRY = gcr.io/${GCLOUD-PROJECT-ID}
PORTS = 8080:8080
TAG = latest
PROJECT_NAME = simple-fastapi
GCLOUD-PROJECT-ID = home-260209
ENV = dev
MEMORY_LIMIT = 50M
ENV_VARIABLES = $(shell ./utils/convert_env.py $(shell pwd)/.env)

activate: 
	pip install --user poetry
	poetry install

test:
	poetry run pytest -vv ${TEST_CASE}

lock:
	poetry lock 

freez: lock
	poetry export -f requirements.txt > requirements.pip

# pre production
build: test freez
	docker build -t ${DOCKER_REGISTRY}/${PROJECT_NAME}:${TAG} .

run:
	poetry run uvicorn project.asgi:app --reload

push: build
	docker push ${DOCKER_REGISTRY}/${PROJECT_NAME}:${TAG}

# deploy
gcloud-deploy: push
	gcloud run deploy ${PROJECT_NAME} --image ${DOCKER_REGISTRY}/${PROJECT_NAME}:${TAG} --memory ${MEMORY_LIMIT} --platform managed --set-env-vars ${ENV_VARIABLES}

gcloud-remove:
	gcloud run service delete ${PROJECT_NAME}
