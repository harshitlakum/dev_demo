APP=dev_demo
IMAGE=ghcr.io/$(shell whoami)/$(APP):latest

.PHONY: help
help:
	@echo "Targets:"
	@echo "  make install        - install app & dev deps"
	@echo "  make lint           - run pre-commit (ruff/black + hygiene)"
	@echo "  make test           - run pytest"
	@echo "  make run            - run uvicorn on :8000"
	@echo "  make docker-build   - build Docker image (dev_demo:local)"
	@echo "  make docker-run     - run container on :8000"
	@echo "  make docker-stop    - stop running container"
	@echo "  make k8s-apply      - apply k8s manifests (namespace: dev-demo)"
	@echo "  make k8s-delete     - delete k8s resources"

install:
	python -m pip install -U pip
	pip install -r requirements.txt
	- pip install -r dev-requirements.txt

lint:
	pre-commit run -a

test:
	pytest -q

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

docker-build:
	docker build -t $(APP):local .

docker-run:
	docker run --rm -d --name $(APP) -p 8000:8000 $(APP):local

docker-stop:
	- docker stop $(APP)

k8s-apply:
	kubectl apply -f k8s/ns.yaml
	kubectl apply -f k8s/deployment.yaml -n dev-demo
	kubectl apply -f k8s/service.yaml -n dev-demo

k8s-delete:
	- kubectl delete -f k8s/service.yaml -n dev-demo
	- kubectl delete -f k8s/deployment.yaml -n dev-demo
	- kubectl delete -f k8s/ns.yaml
