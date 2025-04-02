from cache import get_redis_connection
from database import get_db_session
from repository import TaskRepository, TaskCache, UserRepository
from service import TaskService
from fastapi import Depends

from service.auth import AuthService
from service.user import UserService


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
        task_cache: TaskCache = Depends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository = task_repository,
        task_cache = task_cache
    )

def get_user_repository()-> UserRepository :
    db = get_db_session()
    try:
        yield UserRepository(db)
    finally:
        db.close()

def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository=user_repository)

def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(user_repository=user_repository)

