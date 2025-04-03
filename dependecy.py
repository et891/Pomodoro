from fastapi.params import Security

from cache import get_redis_connection
from database import get_db_session
from exeption import TokenExpired, TokenNotCorrect
from repository import TaskRepository, TaskCache, UserRepository
from service import TaskService
from fastapi import Depends, Request, security, HTTPException

from service.auth import AuthService
from service.user import UserService
from settings import Settings


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

def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(user_repository=user_repository, settings=Settings())

def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)

reusable_oath2 = security.HTTPBearer()

def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oath2)
    ) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired as e:
        raise HTTPException(status_code=401,
                            detail=e.detail)
    except TokenNotCorrect as e:
        raise HTTPException(status_code=401,
                            detail=e.detail)

    return user_id