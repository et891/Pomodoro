from http.client import HTTPException

from dependecy import get_task_service, get_tasks_repository, get_tasks_cache_repository
from repository import TaskRepository, TaskCache
from fastapi import FastAPI, APIRouter, status,Depends
from pydantic import BaseModel
from typing import Annotated
from fixtures import tasks as fixtures_tasks
from schema.task import TaskSchema
from service.task import TaskService

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/all", response_model=list[TaskSchema])
async def get_tasks(task_service: Annotated[TaskService, Depends(get_task_service)]):
    return task_service.get_tasks()

@router.post("/", response_model=TaskSchema)
async def create_task(task: TaskSchema, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
                      task_cache: Annotated[TaskCache, Depends(get_tasks_cache_repository)]
                      ):
    task_id = task_repository.create_task(task)
    task.id = task_id
    task_cache.clear_tasks()  # 👈 очищаем кэш после добавления
    return task

@router.patch("/{task_id}")
async def patch_task(task_id:int,name:str, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    return task_repository.update_task_name(task_id,name)



@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id:int, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    task_repository.delete_task(task_id)
    return {"message":"task deleted successfully"}