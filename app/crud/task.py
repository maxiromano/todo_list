## CRUD TO-DO LIST ##
from bson import ObjectId

from models.task import TaskBase
from db.database import db_client
from schemas.task import task_schema,tasks_schema

async def search_task(field:str,key):
    try:
        task = db_client.local.todo_list.find_one({field:key})
        if task:
            return TaskBase(**task_schema(task))
    except:
        return None

async def create_task(task: TaskBase):
    task_dict = dict(task)
    result = db_client.local.todo_list.insert_one(task_dict)
    return {**task_dict,"id":str(result.inserted_id)}


async def get_all_task():
    # Obtener todos los documentos del cursor   
    return tasks_schema(db_client.local.todo_list.find())



async def get_task(task_id:str):
    task = await search_task("_id",ObjectId(task_id))
    return task


async def update_task(task):
    task_dict = dict(task)
    task_dict.pop("id",None)
    
    try:
        result = db_client.local.todo_list.find_one_and_replace({"_id":ObjectId(task.id)},task_dict)
        return await search_task("_id",ObjectId(task.id))
    except:
        return None

async def delete_task(task_id:str):
    if search_task("_id",ObjectId(task_id)):
        result = db_client.local.todo_list.find_one_and_delete({"_id":ObjectId(task_id)})
    else:
        return {"error":"No se ha eliminado"}