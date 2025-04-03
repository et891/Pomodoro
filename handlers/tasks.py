
from dependecy import get_task_service, get_tasks_repository, get_tasks_cache_repository, get_request_user_id
from repository import TaskRepository, TaskCache
from fastapi import FastAPI, APIRouter, status, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
from fixtures import tasks as fixtures_tasks
from schema import TaskCreateSchema
from schema import TaskSchema
from service.task import TaskService

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/all", response_model=list[TaskSchema])
async def get_tasks(task_service: Annotated[TaskService, Depends(get_task_service)]):
    return task_service.get_tasks()

@router.post("/", response_model=TaskSchema)
async def create_task(body: TaskCreateSchema, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
                      task_servive: Annotated[TaskService, Depends(get_task_service)],
                      task_cache: Annotated[TaskCache, Depends(get_tasks_cache_repository)],
                      user_id:int =Depends(get_request_user_id)
                      ):
    task = task_servive.create_task(body, user_id)
    task_cache.clear_tasks()  # 👈 очищаем кэш после добавления
    return task

@router.patch("/{task_id}")
async def patch_task(
        task_id:int,
        name:str,
        task_servive: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)

):
    try:
        return task_servive.update_task_name(task_id = task_id,name=name, user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id:int,
        task_servive: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)

):
    try:

        task_servive.delete_task(task_id = task_id,user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )