# DevOps Showcase — dev_demo

![CI](https://github.com/harshitlakum/dev_demo/actions/workflows/ci.yml/badge.svg)

FastAPI microservice with tests, Docker, Prometheus `/metrics`, and GitHub Actions that lint, test, build, and push an image to GHCR — clean, free, and corporate-ready.

---

## TL;DR (pick one)

**Local (uvicorn)**

```bash
uvicorn app.main:app --reload --port 8000
```

**Docker (local build)**

```bash
docker build -t dev_demo:local .
docker run --rm -p 8000:8000 --name dev_demo dev_demo:local
```

**From GHCR**

```bash
docker pull ghcr.io/harshitlakum/dev_demo:latest
docker run --rm -p 8000:8000 --name dev_demo ghcr.io/harshitlakum/dev_demo:latest
```

---

## Features

* **FastAPI** service with `/healthz`, `/echo`, and **Prometheus** `/metrics`
* **Quality gates**: pytest, ruff, black via **pre-commit** hooks
* **Containers**: slim **Dockerfile** + `.dockerignore`
* **CI/CD**: GitHub Actions → lint ➜ test ➜ build ➜ **push to GHCR**
* **Makefile** shortcuts for everyday commands
* **Kubernetes (optional)**: simple Deployment + Service for local demo (minikube)

---

## Endpoints

* `GET /healthz` → `{"status":"ok"}`
* `POST /echo` with `{"msg":"hello"}` → `{"msg":"hello","length":5}`
* `GET /metrics` → Prometheus text (includes `http_requests_total`, `http_request_duration_seconds`)

Examples:

```bash
curl -s http://127.0.0.1:8000/healthz
curl -s -X POST http://127.0.0.1:8000/echo -H 'content-type: application/json' -d '{"msg":"devops"}'
curl -s http://127.0.0.1:8000/metrics | head
```

---

## Project layout

```
dev_demo/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_app.py
│   └── test_metrics.py
├── k8s/
│   ├── ns.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── .github/workflows/ci.yml
├── .pre-commit-config.yaml
├── Dockerfile
├── Makefile
├── pyproject.toml
├── requirements.txt
└── dev-requirements.txt
```

---

## Local development

```bash
# (optional) create / activate your env
# conda activate pro_env  OR  python -m venv .venv && source .venv/bin/activate

pip install -r requirements.txt
pip install -r dev-requirements.txt
pre-commit install

# run tests
pytest -q   # expected: 3 passed

# run service
uvicorn app.main:app --reload --port 8000
```

> Note: The first `pre-commit run -a` may auto-fix files and exit non-zero. Run it again and commit.

---

## Makefile (one-liners)

```bash
make install      # pip install -r requirements.txt (+ dev)
make lint         # pre-commit (ruff/black + hygiene)
make test         # pytest
make run          # uvicorn on :8000
make docker-build # build dev_demo:local
make docker-run   # run container on :8000
make docker-stop  # stop container
make k8s-apply    # kubectl apply (namespace: dev-demo)
make k8s-delete   # delete k8s resources
```

---

## Docker

**Build & run locally**

```bash
docker build -t dev_demo:local .
docker run --rm -p 8000:8000 --name dev_demo dev_demo:local
# stop:
docker stop dev_demo
```

**Troubleshooting**

* “port already in use” → change host port: `-p 8001:8000`
* “name already in use” → `docker rm -f dev_demo` or `make docker-stop`

---

## CI/CD & GHCR

* Workflow: `.github/workflows/ci.yml`

  * **test-lint**: install deps → pre-commit → pytest
  * **build-and-push**: Docker buildx → login to GHCR (via `GITHUB_TOKEN`) → push
* Image tags:

  * `ghcr.io/harshitlakum/dev_demo:latest`
  * `ghcr.io/harshitlakum/dev_demo:<commit-sha>`

**Repo settings (once)**
Settings → Actions → General → Workflow permissions → **Read and write permissions**.

---

## Kubernetes (optional, minikube)

```bash
# start minikube if needed
minikube status || minikube start

# load local image into minikube’s Docker
minikube image load dev_demo:local

# apply manifests
make k8s-apply

# wait & port-forward
kubectl -n dev-demo rollout status deploy/dev-demo
kubectl -n dev-demo port-forward deploy/dev-demo 8000:8000 &
curl -s http://127.0.0.1:8000/healthz
```

---

## Tech notes

* **Python** 3.12, **FastAPI** 0.115.x, **Uvicorn** 0.30.x
* **Pre-commit** with **ruff** (lint + import sort) & **black**
* **Prometheus** client: request counter + latency histogram via ASGI middleware
* **Docker**: `python:3.12-slim`, non-root user, smallest practical base

---

## License

MIT.
