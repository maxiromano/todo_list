from fastapi import FastAPI
from endopoints import task

app = FastAPI()

## Routers

app.include_router(task.router)


## Welcome
@app.get("/")
async def hi():
    return "Welcome to my to-do list API"