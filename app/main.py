from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="dev_demo")


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
