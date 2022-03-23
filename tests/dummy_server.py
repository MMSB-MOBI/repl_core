from fastapi import FastAPI
from pydantic import BaseModel
import asyncio 
import concurrent
import functools


from typing import Optional
from time import sleep
from threading import Thread

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





##https://stackoverflow.com/questions/63169865/how-to-do-multiprocessing-in-fastapi
## https://bbc.github.io/cloudfit-public-docs/asyncio/asyncio-part-5.html
#from multiprocessing.pool import ThreadPool
#pool = ThreadPool(processes=1)

SLEEP_MAX = 10

def be_busy(item_id):
    global STORE

    for i in range(SLEEP_MAX):
        sleep(1)
        print(f"Changing {item_id} from {STORE[item_id]} to { STORE[item_id] - 1}")
        STORE[item_id] = STORE[item_id] - 1

STORE = {}

@app.get("/busy/{item_id}")
async def store_item(item_id): 
   
    if not item_id in STORE:
        STORE[ item_id ] = SLEEP_MAX
        loop = asyncio.get_event_loop()
        #with concurrent.futures.ProcessPoolExecutor() as pool:
        #    loop.run_in_executor(pool, functools.partial(be_busy, item_id))  # wait result
        loop.run_in_executor(None, functools.partial(be_busy, item_id))  # wait result  
    
    return {"item_id" : item_id, "status" : STORE[item_id] }

@app.post("/post_busy/")
async def store_item_too(crate:Stuff): 
   
    if not crate.name in STORE:
        STORE[ crate.name ] = SLEEP_MAX
        loop = asyncio.get_event_loop()
        #with concurrent.futures.ProcessPoolExecutor() as pool:
        #    loop.run_in_executor(pool, functools.partial(be_busy, item_id))  # wait result
        loop.run_in_executor(None, functools.partial(be_busy, crate.name))  # wait result  
    
    return {"item_id" : crate.id, "status" : STORE[crate.name], "max_val" : SLEEP_MAX }
    {elem_number}