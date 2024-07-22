### ENDPOINTS ###

from fastapi import APIRouter, HTTPException,Depends
from models.task import TaskBase
from crud.task import create_task, get_all_task, get_task, update_task, delete_task
from models.user import User
from auth.utils import current_user


router = APIRouter()

@router.post("/tasks", response_model=TaskBase)
async def add_task(task:TaskBase, user: User = Depends(current_user)):
    return await create_task(task)

@router.get("/tasks")
async def list_all_tasks(user: User = Depends(current_user)):
    tasks = await get_all_task()
    return tasks

@router.get("/tasks/{id}")
async def search_task(id:str,user: User = Depends(current_user)):
    task = await get_task(id)
    return task

@router.put("/tasks/")
async def replace_task(task:TaskBase,user: User = Depends(current_user)):
    result = await update_task(task)
    return result

@router.delete("/tasks/{id}")
async def eliminate_task(id:str,user: User = Depends(current_user)):
    task = await delete_task(id)
    return task

# gracias a user: User = Depends(current_user) debemos pasarle un bearer token para poder realizar las requests