from cache import get_redis_connection
from database import get_db_session
from repository import TaskRepository, TaskCache
from service import TaskService
from fastapi import Depends

def get_tasks_repository():
    db = get_db_session()
    try:
        yield TaskRepository(db)
    finally:
        db.close()


def get_tasks_cache_repository() -> TaskRepository:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)

def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache: TaskCache = gitDepends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository = task_repository,
        task_cache = task_cache
    )