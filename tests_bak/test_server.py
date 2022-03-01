from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get("/handshake")
def check_conn():
    return "pong"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}