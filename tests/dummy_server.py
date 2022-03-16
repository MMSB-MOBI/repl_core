from fastapi import FastAPI
from pydantic import BaseModel

from typing import Optional

app = FastAPI()

@app.get("/handshake")
def check_conn():
    return "pong"

@app.get("/hello")
def hello():
    return "bonjour"

@app.get("/greetings/{firstname}/{lastname}")
def read_item(firstname: str, lastname:str):
    return f"Hello to you {firstname} -- {lastname}"

class Stuff(BaseModel):
    id : int
    name : str

@app.post("/put_stuff")
def read_item(crate:Stuff):
    return {"status": "SUCCESS", "data":crate}
