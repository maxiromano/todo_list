### ENDPOINTS ###

from fastapi import APIRouter, HTTPException
from models.task import TaskBase
from crud.task import create_task, get_all_task, get_task, update_task

router = APIRouter()

@router.post("/tasks", response_model=TaskBase)
async def add_task(task:TaskBase):
    return await create_task(task)

@router.get("/tasks")
async def list_all_tasks():
    tasks = await get_all_task()
    return tasks

@router.get("/tasks/{id}")
async def search_task(id:str):
    task = await get_task(id)
    return task

@router.put("/tasks/")
async def replace_task(task:TaskBase):
    result = await update_task(task)
    return result
