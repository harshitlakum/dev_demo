import time

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel

app = FastAPI(title="dev_demo")

# ---- Metrics ----
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Request latency in seconds", ["endpoint"]
)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    # label values must be strings
    REQUEST_COUNT.labels(request.method, request.url.path, str(response.status_code)).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(duration)
    return response


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ---- App routes ----
class EchoIn(BaseModel):
    msg: str


class EchoOut(BaseModel):
    msg: str
    length: int


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/echo", response_model=EchoOut)
def echo(payload: EchoIn):
    m = payload.msg
    return {"msg": m, "length": len(m)}
