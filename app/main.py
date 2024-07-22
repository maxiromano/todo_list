from fastapi import FastAPI
from endopoints import task
from auth import utils

app = FastAPI()

## Routers

app.include_router(task.router)
app.include_router(utils.router)

## Welcome
@app.get("/")
async def hi():
    return "Welcome to my to-do list API"